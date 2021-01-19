import sys
import requests
from icalendar import Calendar, vText

def parse_event_description(event):
    description_lines = event['DESCRIPTION'].strip().split('\n')

    # Turn the raw lines into list of lists with 2 elements
    raw_description_entries = list(map(lambda line: line.split(': '), description_lines))
    description_entries = list(map(lambda entry: [entry[0].strip(), entry[1].strip()], raw_description_entries))

    # Turn the list of lists with 2 elements to a dictionary instead
    description_elements = {entry[0]: entry[1] for entry in description_entries}

    return description_elements

def generate_new_lecture_name(lecture_name, lecture_type):
    # Assumes that lecture_name will always be defined
    return (lecture_name + " " + lecture_type) if lecture_type is not None else lecture_name

def ical_to_string(ical):
    return ical.to_ical().decode("utf-8")

url = sys.argv[1]
calendar = requests.get(url).text
cal = Calendar.from_ical(calendar)

for event in cal.walk('VEVENT'):
    description = parse_event_description(event)

    lecture_name = description.get('Description')
    lecture_type = description.get('Event type')

    if lecture_name is not None:
        new_lecture_name = generate_new_lecture_name(lecture_name, lecture_type)
        event['SUMMARY'] = vText(new_lecture_name)

print(ical_to_string(cal))
