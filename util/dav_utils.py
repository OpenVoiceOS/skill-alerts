# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import datetime as dt
import os
from urllib.parse import urlparse
from typing import Set, Optional, Union, List

import icalendar
import caldav
from dateutil.tz import gettz
from json_database import JsonStorage
from ovos_config.locale import get_default_tz
from ovos_utils.time import to_system
from ovos_utils.log import LOG

from ovos_skill_alerts.util import AlertType, DAVType

_DAV_DEFAULT_LOOKAHEAD = 365
_DAV_CREDFILE = "dav_credentials.json"
_DAV_CRED_DEFAULT = {"url": "", "username": "", "password": "", "ssl_verify_cert": ""}


def get_dav_items(calendar: caldav.objects.Calendar, timespan: int = None):
    """
    Get the events and todos from a specific DAV calendar
    :param calendar: caldav calendar object
    :param timespan: the timespan when searching for events (optional)
    :returns: list of Alert objects
    """
    from .alert import Alert

    now = dt.datetime.now(tz=get_default_tz())
    events = calendar.date_search(
        now, now + dt.timedelta(days=timespan or _DAV_DEFAULT_LOOKAHEAD)
    )
    events = [
        event.icalendar_instance.subcomponents[0].property_items() for event in events
    ]
    for event in events:
        event.append(("DAV_CALENDAR", calendar.name))
        event.append(("DAV_SERVICE", calendar.id))
    _todos = calendar.todos(sort_keys=False)
    todos = list()
    # bug upstream where VTIMEZONE events are sent too
    for todo in _todos:
        properties = todo.icalendar_instance.subcomponents[0].property_items()
        if properties[0] == ("BEGIN", b"VTODO"):
            properties.append(("DAV_CALENDAR", calendar.name))
            properties.append(("DAV_SERVICE", calendar.id))
            todos.append(properties)

    alerts = [Alert.from_ical(event) for event in events]
    alerts.extend(_add_relations(todos))
    return alerts


def process_ical_todo(event: List[tuple]) -> dict:
    """
    get a dict representation of an caldav icalendar todo event
    :param properties: tuple of icalendar properties
    :returns: dict
    """
    data = dict(context=dict())
    properties = _convert_ical_datatypes(event)
    
    data["dav_type"] = DAVType.VTODO
    if properties.get("CREATED", False):
        data["context"]["created"] = properties["CREATED"].timestamp()
    elif properties.get("DTSTAMP", False):
        data["context"]["created"] = properties["DTSTAMP"].timestamp()
    # The property "DUE" is equivalent to "DTSTART" of events
    # ie the time until a VTodo entry should be finished
    if properties.get("DUE", False):
        data["expiration"] = properties["DUE"]
        data["alert_type"] = AlertType.REMINDER
    else:
        data["alert_type"] = AlertType.TODO

    data["alert_name"] = properties["SUMMARY"]
    data["context"]["ident"] = properties["UID"]
    if properties.get("PRIORITY", False):
        prio = properties["PRIORITY"]
        data["priority"] = -prio + 10
    if properties.get("RELATED-TO", False):
        data["context"]["related_to"] = properties["RELATED-TO"]
    if properties.get("DAV_CALENDAR", False):
        data["dav_calendar"] = properties["DAV_CALENDAR"]
    if properties.get("DAV_SERVICE", False):
        data["dav_service"] = properties["DAV_SERVICE"]
    return data


def process_ical_event(event: List[tuple]) -> dict:
    """
    get a dict representation of an caldav icalendar event
    :param properties: tuple of icalendar properties
    :returns: dict
    """
    data = dict(context=dict())
    properties = _convert_ical_datatypes(event)

    data["dav_type"] = DAVType.VEVENT
    data["alert_type"] = AlertType.REMINDER

    if properties.get("CREATED", False):
        data["context"]["created"] = properties["CREATED"].timestamp()
    elif properties.get("DTSTAMP", False):
        data["context"]["created"] = properties["DTSTAMP"].timestamp()
    data["expiration"] = properties["DTSTART"]
    if properties.get("DTEND", False):
        data["until"] = properties["DTEND"]
        data["alert_type"] = AlertType.EVENT

    if properties.get("TRIGGER", False):
        delta = properties["TRIGGER"]  # type: dt.timedelta
        delta = int(delta.total_seconds())
        # negative delta (or 0)
        data["prenotification"] = delta or None

    data["alert_name"] = properties["SUMMARY"]
    data["context"]["ident"] = properties["UID"]
    if properties.get("DAV_CALENDAR", False):
        data["dav_calendar"] = properties["DAV_CALENDAR"]
    if properties.get("DAV_SERVICE", False):
        data["dav_service"] = properties["DAV_SERVICE"]
    return data


def _convert_ical_datatypes(event):
    properties = dict(event)

    for k, v in properties.items():
        if isinstance(v, icalendar.vText):
            properties[k] = str(v)
        elif isinstance(v, icalendar.vDDDTypes):
            timedata = v.dt
            if not timedata.__class__ == dt.date and \
                    not isinstance(timedata, dt.timedelta) and \
                    timedata.tzinfo != get_default_tz():
                timedata = to_system(timedata)
            properties[k] = timedata
        
    return properties


def _build_dt_from_date(date, properties):
    """
    Convert datetime.date ("whole day reminder") into datetime.datetime
    Try to get the timezone from the description or use the mycroft 
    level default
    """
    dt_ = dt.datetime.combine(date, dt.time.min)
    descriptions = properties.get("DESCRIPTION", "").split("/n")
    for description in descriptions:
        timezone = gettz(description)
        if timezone is not None:
            break
    return dt_.replace(tzinfo=timezone or get_default_tz())


def _add_relations(events: List[List[tuple]]):
    """
    Helper to deploy additional contextual information about their
    relationship (parent/child)
    :param events: list of caldav icalendar instance properties
    :returns: list of Alert objects
    """
    from .alert import Alert

    alerts = list()
    _children = dict()  # sublist items have to be merged after the fact
    for item in events:
        alert = Alert.from_ical(item)  # type: Alert
        # get parent uuid
        base_uuid = alert.context.get("related_to", False)
        if base_uuid:
            if not base_uuid in _children:
                _children[base_uuid] = set()
            _children[base_uuid].add((alert.ident))
        alerts.append(alert)
    # adding children to parent alerts
    for alert in alerts:
        if alert.ident in _children:
            for uuid in _children[alert.ident]:
                alert.add_child(uuid)

    return alerts


class DAVCredentials(JsonStorage):
    def __init__(self, basedir: str, services: list) -> None:
        credfile = os.path.join(basedir, _DAV_CREDFILE)
        super().__init__(credfile)
        if not os.path.exists(credfile):
            # prepopulate the credentials file
            self.init_credentials(services)

    def init_credentials(self, services):
        for service in services:
            if not self.get(service, False):
                self[service] = _DAV_CRED_DEFAULT
                self.store()
    
    @property
    def empty(self):
        return not any(self.keys())
    
    def viable(self, service: str) -> bool:
        required = ("url", "username", "password")
        credentials = self.get(service, False)
        if not credentials:
            return False
        
        populated = any(credentials[key] != "" for key in required)
        result = urlparse(credentials["url"])
        url_viable = all([result.scheme, result.netloc])
        if not url_viable:
            LOG.error("DAV URL is not viable")
        return populated and url_viable
