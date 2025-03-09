import re

str1 = "/tag/Indie-Pop?start=440&type=T"

pages = str1.split('=')[-2].split('&')[-2]

pattern = r'start=(\d+)'
match = re.search(pattern, str1)
print(pages)
print(match)
if match:
    start_value = match.group(1)
    print(type(start_value))
    print(start_value)
else:
    print("No match found.")