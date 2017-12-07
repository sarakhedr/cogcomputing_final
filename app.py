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

	data = request.data

	diaryEntryJSON = {}
	diaryEntryJSON["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
	diaryEntryJSON["text"] = []
	response = requests.post('https://stream.watsonplatform.net/speech-to-text/api/v1/recognize', headers=headers, data=data, auth=('9cd8ec3d-2d11-4884-8f07-fb4ed37c2add', 'Y33pRZN5DizL'))
	results = json.loads(response.text)["results"]
	
	fullDiaryEntry = ""
	for a in results:
		print(a)
		confidence = a["alternatives"][0]["confidence"]
		text = a["alternatives"][0]["transcript"]
		entry = {}
		entry["confidence"] = confidence
		entry["text"] = text
		diaryEntryJSON["text"].append(entry)
		fullDiaryEntry = fullDiaryEntry + text

	print(diaryEntryJSON)
	
	tone_analyzer(fullDiaryEntry)

	
	response = app.response_class(
		response = "Successful entry",
		status = 200,
		mimetype='application/json'
	)

	return response


def tone_analyzer(diaryEntry):

	headers = {
    'Content-Type': 'application/json',
	}
	params = {"sentences": False}

	diaryJSON = { "text": diaryEntry}

	response = requests.post('https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21', headers=headers, params=params, data=json.dumps(diaryJSON), auth=('e5cba311-14eb-430c-9796-e9a6928cbc34', '3fCSph25MIyS'))


	print(response.text)

	response = json.loads(response.text)

	tones = response["document_tone"]["tones"]

	#emotionsList = []
	toneDict = {}
	toneDict["tones"] = []
	for i in tones:
		score = i["score"]
		name = i["tone_name"]
		toneData = {}	
		toneData["tone"] = name
		toneData["score"] = score
		toneDict["tones"].append(toneData)

	print(toneDict)
	return toneDict
	#return {}


def natural_language_understanding(diaryEntry):
	
"""
journalText ="I am a happy person.  Life is good. I can't wait until the weekend.  I am going to Home Depot to get paint supplies"

featuresJSON = { "entities": { "emotion": True, "sentiment": True}, "keywords": {"emotion": True, "sentiment": True}, "concepts" :{}}

params = { 'text': journalText, 'features': featuresJSON}

headers = {'content-type': 'application/json'}



response = requests.post('https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2017-02-27', data=json.dumps(params), auth=('e75712e0-ea3c-4c29-bc12-950198a900ef', 'HeTGScuehCDq'), headers=headers)

print(response.text)

"""

	return {}



if __name__ == '__main__':
    app.run(port=80, debug=True)
