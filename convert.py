import sys
import requests
from icalendar import Calendar

url = sys.argv[1]
calendar = requests.get(url).text
ical = Calendar.from_ical(calendar)

print(ical)
