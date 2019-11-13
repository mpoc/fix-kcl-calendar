# KCL timetable calendar fixer

This program downloads your KCL timetable calendar from `https://mytimetable.kcl.ac.uk/` and makes the calendar events have pretty names.

Example of an unchanged calendar event name: `5CCS2PEP PRACTICAL EXPER SEM1 000001/LECTURE/01 (STRAND BLDG S-2.18)`

Example of a changed calendar event name: `Practical Experiences of Programming Lecture`

I put the adjusted calendar on my website and import the it into my Google Calendar with a link. I also set up a cronjob to run this every day in case the calendar changes.

## How to build

```console
gradle build
```

Alternatively, this will package all the code and dependendencies into one `jar` file:

```console
gradle fatJar
```

The `jar` file packaged with the dependencies will be located in `build/libs/fix-kcl-calendar-all.jar`.
