import requests
from bs4 import BeautifulSoup
import json
import dateparser

try:
	result = json.loads(open('result.json','r').read())
except:
	result = {}

url = 'https://kemkes.go.id'

r = requests.get(url)
data = r.content

soup = BeautifulSoup(data, 'html.parser')

info = soup.find_all('li', {'class': 'info-case'})

index = 0
for idx,inf in enumerate(info):
	if 'vaksinasi' in inf.text.lower():
		index = idx

table = info[index]

trs = table.find_all('tr')

date = soup.find('li', {'class': 'info-date'})
date = dateparser.parse(date.text.lower().replace('kondisi','').strip()).strftime('%Y-%m-%d')
if not date in result.keys():
	result[date] = {}
	for tr in trs:
		description = tr.find('td', {'class': 'description'})
		case        = tr.find('td', {'class': 'case'})
		if not description.text in result[date].keys():
			result[date][description.text] = int(case.text.replace('.',''))

with open('result.json', 'w') as fle:
	fle.write(json.dumps(result, indent=4))

