from dateutil.tz import gettz
import datetime as dt
from typing import List

from ovos_config.config import Configuration
from ovos_config.locale import get_default_tz
from ovos_utils.file_utils import resolve_resource_file

DEFAULT_SETTINGS = {
    "speak_alarm": False,
    "speak_timer": True,
    "sound_alarm": "constant_beep.mp3",
    "sound_timer": "beep4.mp3",
    "snooze_mins": 15,
    "timeout_min": 1,
    "play_volume": 90,
    "escalate_volume": True,
    "priority_cutoff": 8,
    "services": "",
    "frequency": 15,
    "sync_ask": False
}


def use_24h_format() -> bool:
    return Configuration()["time_format"] == "full"


def get_date_format() -> str:
    return Configuration()["date_format"]


def find_resource_file(name: str, extensions: List[str] = None):
    name = name.lower()
    if extensions is None:
        extensions = []
    for ext in extensions:
        filename = resolve_resource_file(f"{name}.{ext}")
        if filename:
            return filename
    else:
        return resolve_resource_file(name)
