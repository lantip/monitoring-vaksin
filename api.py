from flask import Flask, jsonify
import pathlib
from datetime import datetime, timedelta
import json
import re


app = Flask(__name__)

def sanitize(string):
	string = re.sub(r'[^A-Za-z0-9 ]+', '', string)
	string = string.lower().replace(' ','_')
	return string

@app.route('/')
def index():
	fname = pathlib.Path('result.json')
	mtime = datetime.fromtimestamp(fname.stat().st_mtime) + timedelta(hours=7)

	record = json.loads(open('result.json','r').read())
	result = []
	for key,recs in record.items():
		rcd = {}
		for k,v in recs.items():
			rcd[sanitize(k)] = v
		rcd['date'] = key
		result.append(rcd)

	return jsonify({
			'last_updated': mtime.strftime('%d-%m-%Y %H:%M:%S'),
			'monitoring': result
		})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
