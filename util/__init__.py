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

from enum import IntEnum, Enum

LOCAL_USER = "local"

class AlertState(IntEnum):
    REMOVED = 0
    MISSED = 1
    PENDING = 2
    ACTIVE = 3


class AlertType(IntEnum):
    ALL = -1
    ALARM = 0
    TIMER = 1
    REMINDER = 2
    EVENT = 3
    TODO = 4
    UNKNOWN = 99


class DAVType(IntEnum):
    VEVENT = 1
    VTODO = 2


class AlertPriority(IntEnum):
    HIGHEST = 10
    AVERAGE = 5
    LOWEST = 1


# This is comparing against fuzzy_match (0-100)
class MatchLevel(IntEnum):
    ALL_EXACT = 120
    DT_EXACT = 111
    NAME_EXACT = 110
    TIME_EXACT = 100


class Weekdays(IntEnum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


WEEKDAYS = {Weekdays.MON, Weekdays.TUE, Weekdays.WED, Weekdays.THU,
            Weekdays.FRI}
WEEKENDS = {Weekdays.SAT, Weekdays.SUN}
EVERYDAY = {Weekdays.MON, Weekdays.TUE, Weekdays.WED, Weekdays.THU,
            Weekdays.FRI, Weekdays.SAT, Weekdays.SUN}
