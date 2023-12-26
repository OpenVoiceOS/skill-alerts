# <img src='./logo.svg' card_color="#FF8600" width="50" style="vertical-align:bottom" style="vertical-align:bottom">Alerts  
  
## Summary  
  
A skill to manage alarms, timers, reminders, events and todos and optionally sync them with a CalDAV service.


## Description  
  
The skill provides functionality to create alarms, timers, reminders and todo (lists), remove them by name, time, or type, and ask for
what is active. If you choose to syncronize with a DAV server, you can also access your reminders and todo lists from other devices.

Alarms and reminders may be set to recur daily or weekly. An active alert may be snoozed for a specified amount of time
while it is active. Any alerts that are not acknowledged will be added to a list of missed alerts that may be read and
cleared when requested.

If you were away, your device was off, or the device was napping, ask for a summary of what was missed. The number of notifications
missed can be seen on the upper left corner of the Home screen. 

### Distinction between reminder, event and todo

<ins>__*Events*__</ins>  
<sub>Appointments, gigs, ... that may (but not necessarily) have a start and end time. Like this you are notified if an e.g. appointment collides with another one. Events may be created with a prenotification in advance</sub>

<ins>__*Reminders*__</ins>  
<sub>Less formal dates that only have a start time.  
(Although you can set a repeating reminder also with an endpoint - eg "remind me to take out the trash every day at 7pm <ins>until</ins> next saturday")</sub>

<ins>__*Todos*__</ins>  
<sub>Non time related "short term memory" for things to do. Todos can be organised in lists. Eg shopping list</sub>

<ins>__*Alert*__</ins>  
<sub>is a bucket term for all of the different types.</sub>

-----------------------

## Scenarios

<ins>Keywords</ins> are underlined, _alert names_ italic  
if not specifically mentioned (like _bread_ timer, _tennis_ event), the name defaults to the time it is set for (eg _8 AM_ alarm, _2 minute_ timer)

### Alarms, Timers, Reminders, Events

*One time* alarms, timers, reminders or events:
- "<ins>Set</ins> an <ins>alarm</ins> for _8 AM_."
- "<ins>Set</ins> a _bread_ <ins>timer</ins> for 30 minutes."
- "<ins>Schedule</ins> a _tennis_ <ins>event</ins> for 2 PM on friday <ins>spanning</ins> 2 hours."
... _(events may be created with a prenotification in advance)_

<sup>HINT:</sup> _A *timer* started without a time specified acts like a stop timer counting up from now.
To stop it and voice the time delta say "Timer stop"._

*Recurring* alarms, reminders or events:
- "<ins>Set</ins> a <ins>daily</ins> <ins>alarm</ins> for _8 AM_."
- "<ins>Set</ins> an <ins>alarm</ins> for 8 AM on <ins>saturdays</ins>."
- "<ins>remind</ins> me to _take out the trash_ <ins>every</ins> Thursday and Sunday at 7 PM."

*OCP* Alarm:  
<sup>(Alarm triggering Media Player; _depends on the OCP capabilities of your device/serveing instance_)</sup>
- "<ins>wake</ins> me up at 8 AM with <ins>music</ins>." (in general: "... with {media type})  
<sub>-> the skill will ask you which media title to play -> lookup media in the media library</sub>
- "<ins>wake</ins> me with <ins>music</ins>." <sub>(_change/set media on an already created alarm_; next alarm will be chosen)</sub>

*Reschedule* an existing alarm, timer, reminder or event:  
<sup>(duration or fixed time)</sup>

- "<ins>Reschedule</ins> my _8 AM_ <ins>alarm</ins> at 9 AM."
- "<ins>Push</ins> the _tennis_ <ins>event</ins> by one hour."
- "<ins>Move</ins> my <ins>next</ins> <ins>event</ins> one hour <ins>earlier</ins>."
- "<ins>Extend</ins> the _bread_ <ins>timer</ins> by 2 minutes." (or: <ins>Extend</ins> the _bread_ <ins>timer</ins> until 10 am)
- "<ins>Change</ins> the _8 AM_ <ins>alarm</ins> <ins>recurring</ins> only mondays and tuesdays."
- "<ins>Change</ins> _tennis_ <ins>event</ins> <ins>length</ins> to 3 hours."

<sup>HINT:</sup> _You can reschedule the time of a recurring alarm and will be asked if that applies to all or just the next one._

*Query*:
- "<ins>When</ins> is my <ins>next</ins> <ins>alarm</ins>?"
- "<ins>Which</ins> <ins>reminders</ins> are scheduled today?"
- "<ins>Are there</ins> any <ins>events</ins> between friday <ins>and</ins> sunday?" (also: "between friday 10am <ins>and</ins> 3 pm")  
<sub>_running timer_</sub>
- "<ins>How much</ins> time is <ins>left</ins> on my _bread_ <ins>timer</ins>?"

*Cancel*:
- <sup>_specific type/name:_</sup> "<ins>Cancel</ins> my _8 AM_ <ins>alarm</ins>." (in general: "cancel my {name} {type}")
- <sup>_all / of a type_:</sup> "<ins>Cancel</ins> <ins>all</ins> <ins>alerts</ins>." / "<ins>Cancel</ins> <ins>all</ins> <ins>alarms</ins>."
- <sup>_on a specific day_:</sup> "<ins>Cancel</ins> <ins>alerts</ins> on saturday."
- <sup>_in a time period_:</sup> "<ins>Cancel</ins> <ins>alerts</ins> between Friday 8 AM <ins>and</ins> 10 AM."
- <sup>_next_:</sup> "<ins>Cancel</ins> my <ins>next</ins> <ins>alarm</ins>."

<sup>CAUTION:</sup> _Double check if you "cancel all", especially when using DAV, as it will drop all of the reminder/events._

*Active alert* (expired and currently speaking or playing):
- <sup>_dismiss_:</sup> "<ins>Stop alert</ins>."
- <sup>_snooze_:</sup> "<ins>Snooze</ins>." (factory default is 15 minutes)
- <sup>_duration_:</sup> "<ins>Snooze</ins> for 1 minute." / "<ins>Snooze</ins> until 8 AM."

<sup>HINT:</sup> _You can also "snooze" an active reminder/timer with "<ins>remind me again</ins> at 10 AM." / "<ins>extend by</ins> 2 minutes".  
The alert name must not be mentioned in this instance. Active alerts are always considerred directly editable._
  
*Missed alerts* (expired and not acknowledged):

- "<ins>Which alert did i miss?</ins>"
- "<ins>Missed any alerts?</ins>"

### Todo

- [x] walk the dog
- [ ] shopping
  - [ ] milk
  - [ ] toast

_(When using nextcloud as DAV server, be sure to use the "Tasks" plugin application)_	

_*Create:*_<sub>
- "<ins>Remind</ins> me to _walk the dog_"
- "<ins>create</ins> a _shopping_ <ins>list</ins>" (with the option to populate the list afterwards)
  
_*Sublist:*_
- "<ins>add</ins> <ins>items</ins> to the _shopping_ <ins>list</ins>" -> _set the items one by one: eg. milk <sup>*pling*</sup> toast <sup>*pling*</sup> .._ <sup>_(silence stops recording)_</sup>  
<sup>_(list is shown on screen/voiced in advance)_</sup>  

_*Complete todos:*_  
- "<ins>scratch</ins> milk <ins>entry</ins> from the _shopping_ <ins>list</ins>"  
- <sup>_Optionally remove one/multiple; list is shown on screen/voiced :_</sup> "<ins>remove</ins> <ins>item(s)</ins> from the _shopping_ <ins>list</ins>"
- <ins>Remove</ins> <ins>all</ins> <ins>items</ins> on the _shopping_ <ins>list</ins>
- <ins>Remove</ins> _shopping_ <ins>list</ins>  
<sub>_analogous for non lists:_</sub>
- "<ins>remove</ins> _walk the dog_ <ins>note</ins>"
- "<ins>remove</ins> <ins>todo</ins> entr(y/ies)"
- "<ins>remove</ins> <ins>all</ins> <ins>memos</ins>"

(if DAV active, marked as complete on server)

_Query:_
* <sup>_list names :_</sup> "<ins>which</ins> <ins>lists</ins> are stored?" _... "shopping"_
* <sup>_list items :_</sup> "<ins>which</ins> <ins>items</ins> are on the _shopping_ <ins>list</ins>?" _... "milk and toast"_
* <sup>_todo items :_</sup> "<ins>Anything</ins> <ins>todo</ins>?" _... "i should remind you to walk the dog"_

### DAV
_Calendar names:_
- <ins>which</ins> <ins>calendars</ins> are <ins>available</ins>?

_Sync:_ (Supposed to run automatically every x minutes, but can be triggered manually)
- <ins>synchronize</ins> <ins>calendars</ins>


---------

## Settings

<sup>_(this is the default)_</sup>
```python
{
    "speak_alarm": false,                              # if the alarm should be spoken
    "speak_timer": true,                               # if the timer should be spoken
    "sound_alarm": "<path/to/soundfile>",              # default constant_beep.mp3
    "sound_timer": "<path/to/soundfile>",              # default beep4.mp3
    "snooze_mins": 15,                                 # default snooze time if duration/time is not specified
    "timeout_min": 1,                                  # the duration the user is notified, after which the alert is considered missed
                                                       # (doesn't apply to media -radio/video/..- alarms)
    "play_volume": 90,                                 # volume of the alert sound
    "escalate_volume": true,                           # alarms only - raise volume over time (10% steps, dependent on timeout_min;
                                                       #                                       half the time on max volume = `play_volume`)
    "priority_cutoff": 8
    ...
}
```
DAV settings see below

## Setting up DAV connection
(tested with NextCloud)

By now, you have to edit the credential file manually, this will change in the future  
With the startup of the skill, a template file will be created under `~/.local/share/mycroft/filesystem/skills/<skillname>/dav_credentials.json`

```python
{
    "<service>": {
        "url": "https://<ip:port>/remote.php/dav",
        "username": "...",
        "password": "...",
        "ssl_verify_cert": "..."                       # if SSL is set up, otherwise delete this line
    },
    "<another service>": ...
}
```

First setup the credentials, then populate respective parts in the skill settings file `settings.json`
the skill setting get reloaded and the repeating sync event starts (every `frequency` seconds)
```python
{
    ...,
    "services": "<service>,<another service>",         # comma separated string of services
    "frequency": 15,                                   # the number of minutes between syncronisation; default 15
    "sync_ask": false                                  # If it should be asked if a generated reminder/todo element should be synchronized
}
```

The skill fetches DAV calendar dates one year in advance.
You can set up multiple calendars on the server, the skill will ask to which it should be synced.
Errors during connection will be voiced, for specifics check the skill log.

Only events, reminder and todos will be synced. Alarms and timers won't be.
Check the timezone on your server/event, as sometimes the timezone is not recognized properly and therefor scheduled incorrectly

## Known Bugs / Troubleshooting

_Generally, this skill is meant for ovos-core >= 0.0.8 and its dependencies. If you are using an older version, please update or you might experience major problems.  
The skill is tested predominantly in german and (to a lesser extent) english, but might lack certain individual speech patterns. Other languages are autotranslated and need to be sanitized. In the alpha phase we like to encourage you to contribute to form a well balanced experience for a wide variety of languages_

- __The skill wont understand/misinterpret what i'm saying.__  
_Check the logs for the intent that was triggered and the utterance that was transcribed. STT might have gotten the words wrong. Maybe change the service (Known issue especially with non english speakers using Whisper)_
- __The notification system is not working properly. Missed alerts are not shown.__  
_The notifications sometimes get mixed up, this is a known issue and it's worked on. Be sure you are using the latest `ovos-gui-plugin-shell-companion` ([#](https://github.com/OpenVoiceOS/ovos-gui-plugin-shell-companion)) and have the old `ovos-PHAL-plugin-notification-widgets` deinstalled._
- __When polpulating a list, the last element is followed by an "unknown" utterance.__  
_This is a known issue and will be fixed in the next release. It's a problem with the way the skill is handling the input in a response context. It's not critical and can be ignored for now. The list is populated correctly most of the time_

## Recommended Versions
These aren't hard requirements as preferences may vary, but recommended
GUI: `skill-ovos-homescreen >= 0.0.3a6` (There is also a [PR](https://github.com/OpenVoiceOS/skill-ovos-homescreen/pull/92) pending)

## Incompatible Skills
This skill has known intent collisions and replaces:
- [skill-reminder.mycroftAI](https://github.com/mycroftai/skill-reminder)
- [skill-alarm.mycroftAI](https://github.com/mycroftai/skill-alarm)
- [mycroft-timer.mycroftAI](https://github.com/mycroftai/mycroft-timer)
- [skill-alerts.NeonGeckoCom](https://github.com//skill-alerts)

Be sure to remove them before installing this skill.

## Contributing Translations
The skill is for the most part autotranslated (except en/de) and needs to be sanitized.  
As the examples above show, the skill is using adapt keywords to determine intent. The [vocabulary]() keywords should include a variety of synonym nouns and verbs to satisfy a wide range of speech patterns.  

Dates and names are parsed either as a leftover (ie. non keyword) or following a keyword (eg. `until.voc` _until 6 AM_)
Noise words that should be ignored parsing a reminder name are listed in `noise_words.voc`  
(eg. "remind <ins>me</ins> <ins>to</ins> take out <ins>the</ins> trash -> `take out trash`)  
_Dialogs_ are straight forward most of the time and should include the correct mustache tags from the get go.  
These are easy patterns to keep in mind.  

If you want to contribute to the translation, please check the `vocab` folder and add the respective files for your language.  
A basic understanding of the intent structure and what to make of it is required.
```python
require("query").one_of("alarm", "reminder", "event", "alert", "remind").optionally("and").optionally("stored")  # <- vocab
```
In the likely case that questions arise, feel free to contact @sgee_ in matrix chat.

## Contact Support
Use [this link (Matrix Chat)](https://matrix.to/#/!XFpdtmgyCoPDxOMPpH:matrix.org?via=matrix.org) or
[submit an issue on GitHub](https://github.com/OpenVoiceOS/skill-alerts/issues)

## Credits
[NeonGeckoCom](https://github.com/NeonGeckoCom)
[NeonDaniel](https://github.com/NeonDaniel)

## Category
**Productivity**
Daily

## Tags
#OVOS
#OpenVoiceOS
#alert
#alarm
#timer
#reminder
#schedule
