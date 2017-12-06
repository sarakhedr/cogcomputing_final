from flask import Flask, render_template, request
import models
import requests
import json
import datetime

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/dashboard")
def dashboard():
	return render_template("dashboard.html")

@app.route('/api/entries', methods=['GET', 'POST'])
def api_entries():
    if flask.request.method == 'GET':
        entries = [entry.to_dict() for entry in models.Entry.select()]
        return flask.jsonify(entries)
    elif flask.request.method == 'POST':
        entry = models.Entry.create(content='Hello world')
        return flask.jsonify(entry.to_dict())

@app.route('/api/audio', methods=['POST'])
def audio_to_text():
	headers = {
    	'Content-Type': 'audio/wav',
	}

	data = request.data#open('audio-file.flac', 'rb').read()

	diaryEntryJSON = {}
	diaryEntryJSON["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
	diaryEntryJSON["text"] = []
	response = requests.post('https://stream.watsonplatform.net/speech-to-text/api/v1/recognize', headers=headers, data=data, auth=('9cd8ec3d-2d11-4884-8f07-fb4ed37c2add', 'Y33pRZN5DizL'))
	results = json.loads(response.text)["results"]
	for a in results:
		print a
		confidence = a["alternatives"][0]["confidence"]
		text = a["alternatives"][0]["transcript"]
		entry = {}
		entry["confidence"] = confidence
		entry["text"] = text
		diaryEntryJSON["text"].append(entry)

	print diaryEntryJSON
	
	response = app.response_class(
		response = "Successful entry",
		status = 200,
		mimetype='application/json'
	)

	return response


if __name__ == '__main__':
    app.run(port=80, debug=True)
