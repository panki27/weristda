#!/usr/bin/python
import re, datetime

PATTERN = "[a-z]+(\d+)"
FILE = "/var/www/felixpankratz/anwesenheit"
yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
if datetime.datetime.today().weekday() == 0:
    with open(FILE, 'r') as f:
        content = f.readlines()
        f.close()
    for line in content[::-1]:
        strippedLine = line.strip()
        match = re.match(PATTERN, strippedLine)
        if match:
            datestr = match.group(1)
            date = datetime.datetime.strptime(datestr, '%Y%m%d')
            if date < yesterday:
                print('removing entry ' + strippedLine)
                content.remove(line)
    with open(FILE, 'w') as f:
        for line in content:
            f.write(line)
        f.close()
