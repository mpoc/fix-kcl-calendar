import sys
import requests
from icalendar import Calendar

url = sys.argv[1]
calendar = requests.get(url).text
ical = Calendar.from_ical(calendar)

def ical_to_string(ical):
    return ical.to_ical().decode("utf-8")

print(ical_to_string(ical))
