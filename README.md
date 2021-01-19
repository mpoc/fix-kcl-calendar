# KCL timetable calendar fixer

This program downloads your KCL timetable calendar from `https://mytimetable.kcl.ac.uk/` and makes the calendar events have pretty names.

Example of an unchanged calendar event name: `5CCS2PEP PRACTICAL EXPER SEM1 000001/LECTURE/01 (STRAND BLDG S-2.18)`

Example of a changed calendar event name: `Practical Experiences of Programming Lecture`

I put the adjusted calendar on my website and import the it into my Google Calendar with a link. I also set up a cronjob to run this every day in case the calendar changes.

## How to run

### Docker

```console
docker run --rm mpoc/fix-kcl-calendar "URL_TO_CALENDAR" > calendar-adjusted.ics
```

### Natively

```console
python3 convert.py "URL_TO_CALENDAR" > calendar-adjusted.ics
```
