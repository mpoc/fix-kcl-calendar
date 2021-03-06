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

# Returns a tuple with (Boolean, String) where the Boolean is whether the name
# should be modified and String is the name it should be modified to
def generate_new_lecture_name(lecture_name, lecture_type):
    if lecture_name is not None and lecture_type is not None:
        return (True, lecture_name + " " + lecture_type)
    elif lecture_name is not None and lecture_type is None:
        return (True, lecture_name)
    else:
        return (False, None)

def guess_lecture_name(event, module_code_map):
    module_code = str(event['SUMMARY'])[:8]
    return module_code_map.get(module_code)

def ical_to_string(ical):
    return ical.to_ical().decode("utf-8")

module_code_map = {
    '4CCS1CIT': 'Circuit Theory',
    '4CCS1CS1': 'Computer Systems I',
    '4CCS1DBS': 'Database Systems',
    '4CCS1DST': 'Data Structures',
    '4CCS1ELA': 'Elementary Logic with Applications',
    '4CCS1FC1': 'Foundations of Computing I',
    '4CCS1ISE': 'Introduction to Software Engineering',
    '4CCS1LOD': 'Logic Design',
    '4CCS1PL1': 'Electronic Applications Project and Engineering Lab 1',
    '4CCS1PPA': 'Programming Practice and Applications',
    '4CCS1PRP': 'Programming Practice',
    '5CCS2ECM': 'Electricity and Magnetism',
    '5CCS2EES': 'Engineering and Entrepreneurial Skills',
    '5CCS2ELC': 'Electronic Circuits',
    '5CCS2ENM': 'Engineering Mathematics',
    '5CCS2FC2': 'Foundations of Computing II',
    '5CCS2INS': 'Internet Systems',
    '5CCS2INT': 'Introduction to Artificial Intelligence',
    '5CCS2ITR': 'Introduction to Robotics',
    '5CCS2OSC': 'Operating Systems and Concurrency',
    '5CCS2PEP': 'Practical Experiences of Programming',
    '5CCS2PL2': 'Electronic Applications Project and Engineering Lab 2',
    '5CCS2PLD': 'Programming Language Design Paradigms',
    '5CCS2POE': 'Principles of Electronics',
    '5CCS2RGP': 'Robotics Group Project',
    '5CCS2SAS': 'Signals and Systems',
    '5CCS2SEG': 'Software Engineering Group Project',
    '6CCS3AIN': 'Artificial Intelligence Reasoning and Decision Making',
    '6CCS3AIP': 'Artificial Intelligence Planning',
    '6CCS3AMS': 'Agents and Multi-Agent Systems',
    '6CCS3BIM': 'Biologically Inspired Methods',
    '6CCS3CFL': 'Compilers and Formal Languages',
    '6CCS3CIS': 'Cryptography and Information Security',
    '6CCS3COS': 'Communication Systems',
    '6CCS3COV': 'Computer Vision',
    '6CCS3DSM': 'Distributed Systems',
    '6CCS3EEP': 'Electronic Engineering Individual Project',
    '6CCS3EGP': 'Group Project',
    '6CCS3ELC': 'Electronic Circuits',
    '6CCS3GRS': 'Computer Graphics Systems',
    '6CCS3HAD': 'Hardware Design',
    '6CCS3HCI': 'Human-Computer Interaction',
    '6CCS3INS': 'Internet Systems',
    '6CCS3NSE': 'Network Security',
    '6CCS3OME': 'Optimisation Methods',
    '6CCS3PAL': 'Parallel Algorithms',
    '6CCS3PRE': 'Pattern Recognition',
    '6CCS3PRJ': 'Individual Project',
    '6CCS3ROS': 'Robotic Systems',
    '6CCS3RSC': 'Real Time Systems & Control',
    '6CCS3SAD': 'Software Architecture and Design',
    '6CCS3SEA': 'Sensors and Actuators',
    '6CCS3SIA': 'Software Engineering of Internet Applications',
    '6CCS3SMT': 'Software Measurement and Testing',
    '6CCS3SPE': 'Agile Software Performance Engineering in Industrial Practice',
    '6CCS3TSP': 'Text Searching and Processing',
    '6CCS3VER': 'Formal Verification',
    '6CCS3WSN': 'Algorithms for the World Wide Web and Social Networks',
    '7CCMMS61T': 'Statistics for Data Analysis',
    '7CCS4EEP': 'Electronic Engineering Individual Project',
    '7CCS4PRJ': 'MSci Individual Project',
    '7CCSMADA': 'Algorithms Design and Analysis',
    '7CCSMAIN': 'Artificial Intelligence',
    '7CCSMAMF': 'Agent Based Modelling in Finance',
    '7CCSMAMS': 'Agents and Multi-Agent Systems',
    '7CCSMART': 'Advanced Research Topics',
    '7CCSMASE': 'Advanced Software Engineering',
    '7CCSMBDT': 'Big Data Technologies',
    '7CCSMBIM': 'Biologically Inspired Methods',
    '7CCSMCFC': 'Computer Forensics and Cybercrime',
    '7CCSMCFP': 'Computational Finance Individual Project',
    '7CCSMCIS': 'Cryptography and Information Security',
    '7CCSMCMB': 'Algorithms for Computational Molecular Biology',
    '7CCSMCMP': 'Computer Programming for Data Scientists',
    '7CCSMCTH': 'Communication Theory',
    '7CCSMCVI': 'Computer Vision',
    '7CCSMDAS': 'Software Design and Architecture',
    '7CCSMDBT': 'Database Technology',
    '7CCSMDCO': 'Digital Communications',
    '7CCSMDDW': 'Databases, Data Warehousing and Information Retrieval',
    '7CCSMDLC': 'Distributed Ledgers and Crypto-Currencies',
    '7CCSMDM1': 'Data Mining',
    '7CCSMDPJ': 'Data Science Project',
    '7CCSMDSI': 'Data Structures and their Implementation in C++',
    '7CCSMDSM': 'Distributed Systems',
    '7CCSMDSP': 'Fundamentals of Digital Signal Processing',
    '7CCSMGPR': 'Group Project',
    '7CCSMHFF': 'High-Frequency Finance',
    '7CCSMIEF': 'Industry expert lectures in Finance',
    '7CCSMML1': 'Machine Learning',
    '7CCSMMPC': 'Mobile & Personal Communications Systems',
    '7CCSMNSE': 'Network Security',
    '7CCSMNTH': 'Network Theory',
    '7CCSMOME': 'Optimisation Methods',
    '7CCSMOPC': 'Optical Communications',
    '7CCSMOPM': 'Operations Management',
    '7CCSMPDA': 'Parallel and Distributed Algorithms',
    '7CCSMPMT': 'Principles of Management',
    '7CCSMPNN': 'Pattern Recognition',
    '7CCSMPRJ': 'Individual Project (MSc Dissertation)',
    '7CCSMPRO': 'Project Management',
    '7CCSMQMF': 'Quantitative Methods in Finance',
    '7CCSMROB': 'Robotics Systems',
    '7CCSMRTS': 'Real Time Systems and Control',
    '7CCSMRVA': 'Random Variables & Stochastic Processes',
    '7CCSMSAI': 'Sensors and Actuators',
    '7CCSMSCF': 'Scientific Computing for Finance',
    '7CCSMSDV': 'Simulation and Data Visualisation',
    '7CCSMSEM': 'Security Management',
    '7CCSMSEN': 'Security Engineering',
    '7CCSMSIA': 'Software Engineering of Internet Applications',
    '7CCSMSUF': 'Software Engineering and Underlying Technology for Financial Systems',
    '7CCSMTDS': 'Topics on Data and Signal Analysis',
    '7CCSMTN1': 'Telecommunications Networks I',
    '7CCSMTN2': 'Telecommunications Networks II',
    '7CCSMTSP': 'Text Searching and Processing',
    '7CCSMWAL': 'Algorithmic Issues in the World Wide Web',
    '7CCSMWIN': 'Web Infrastructure',
    '6CCS3MDE': 'Model-driven Engineering',
    '6CCS3ML1': 'Machine Learning'
}

event_type_map = {
    'Online Live Tutorial': 'LGT',
    'Online Live Small Group': 'SGT',
    # I'm not sure if this is actually a practical
    'Online Live Workshop': 'Practical'
}

url = sys.argv[1]
calendar = requests.get(url).text
cal = Calendar.from_ical(calendar)

for event in cal.walk('VEVENT'):
    description = parse_event_description(event)

    # Attempt to extract the module name
    lecture_name = guess_lecture_name(event, module_code_map) or description.get('Description') or None
    
    # Attempt to get the event type
    # If there is a mapping of that event type, assign remapped event type
    # If there is no mapping, assign the raw event type
    # If there is no event type, assign None
    raw_event_type = description.get('Event type')
    lecture_type = event_type_map.get(raw_event_type, raw_event_type) or None

    lecture_name_modifier = generate_new_lecture_name(lecture_name, lecture_type)
    name_should_be_modified = lecture_name_modifier[0]
    new_lecture_name = lecture_name_modifier[1]

    if name_should_be_modified:
        event['SUMMARY'] = vText(new_lecture_name)

print(ical_to_string(cal))
