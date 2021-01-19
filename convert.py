import sys
import requests




url = sys.argv[1]
calendar = requests.get(url).text

print(calendar)
