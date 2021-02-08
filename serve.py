from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
	record = json.loads(open('result.json','r').read())
	result = []
	for key,recs in record.items():
		recs['tanggal'] = key
		result.append(recs)
	return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
