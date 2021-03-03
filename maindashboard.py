import requests
from bs4 import BeautifulSoup
import json
import os, re
from datetime import datetime
import dateparser
import shutil
from ocr_kemkes import ocr_date

dir_path = os.path.dirname(os.path.realpath(__file__))

def sanitize(string):
    string = re.sub(r'[^A-Za-z0-9 ]+', '', string)
    string = string.lower().replace(' ','_')
    return string

try:
    result = json.loads(open(dir_path+'/result.json','r').read())
except:
    result = {}
baseurl = 'https://www.kemkes.go.id/'
url = 'https://www.kemkes.go.id/article/view/21030300004/Situasi-Vaksinasi-COVID-19.html'

skrg = datetime.now().strftime('%Y-%m-%d')

if not os.path.isfile(dir_path+'/data/'+skrg+'.png'):
    if not os.path.isfile(dir_path+'/data/'+skrg+'.jpg'):

        r = requests.get(url)
        data = r.content

        soup = BeautifulSoup(data, 'html.parser')

        fto = soup.find('img', {'alt': 'vaksin'})

        foto = baseurl+fto.attrs['src']
        
        filename = skrg+'.'+foto.split('.')[len(foto.split('.'))-1]
        r = requests.get(foto, verify=False, stream=True)
        if r.status_code == 200:
            with open(dir_path+'/data/'+filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)  

today_result = ocr_date(dir_path+'/data/'+skrg+'.png')

if not today_result['date'] in result.keys():
    result[today_result['date']] = {}
    for key, val in today_result.items():
        if key != 'date':
            if not key in result[today_result['date']].keys():
                result[today_result['date']][key] = val

    with open(dir_path+'/result.json', 'w') as fle:
        fle.write(json.dumps(result, indent=4))
