from flask import Flask, render_template, request, jsonify
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


@app.route('/api/entries')
def api_entries():
	jsonEntries = []
	for entry in models.Entry.select():
		jsonEntry = {
		'text': json.loads(entry.text),
		'tone_analysis': json.loads(entry.tone_analysis),
		'nlu_analysis': json.loads(entry.nlu_analysis),
		'time': entry.time,
		}
		jsonEntries.append(jsonEntry)
	return jsonify(jsonEntries)


@app.route('/api/text', methods=['POST'])
def text():
	textEntry = request.data.decode('utf-8')
	text = [{"text": textEntry, "confidence": 1.0}]

	tone = tone_analyzer(textEntry)
	nlu = natural_language_understanding(textEntry)

	entry = models.Entry.create(
		text=json.dumps(text),
		tone_analysis=json.dumps(tone),
		nlu_analysis=json.dumps(nlu),
	)

	response = app.response_class(
		response = json.dumps({}),
		status = 200,
		mimetype='application/json'
	)

	return response


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
		# print(a)
		confidence = a["alternatives"][0]["confidence"]
		text = a["alternatives"][0]["transcript"]
		entry = {}
		entry["confidence"] = confidence
		entry["text"] = text
		diaryEntryJSON["text"].append(entry)
		fullDiaryEntry = fullDiaryEntry + text

	# print(diaryEntryJSON)

	# print fullDiaryEntry
	tone_analyzer(fullDiaryEntry)
	natural_language_understanding(fullDiaryEntry)


	response = app.response_class(
		response = json.dumps({}),
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

	# print(toneDict)
	# print toneDict
	return toneDict


def natural_language_understanding(diaryEntry):

	featuresJSON = { "entities": { "emotion": True, "sentiment": True}, "keywords": {"emotion": True, "sentiment": True}, "concepts" :{}}
	params = { 'text': diaryEntry, 'features': featuresJSON}
	headers = {'content-type': 'application/json'}
	response = requests.post('https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2017-02-27', data=json.dumps(params), auth=('e75712e0-ea3c-4c29-bc12-950198a900ef', 'HeTGScuehCDq'), headers=headers)

	data = {}
	data["keywords"] = []
	data["entities"] = []
	response = json.loads(response.text)

	# Parse keywords
	for k in response["keywords"]:
		keywordData = {}

		keyword = k["text"]
		relevance = k["relevance"]
		emotions = compute_top_emotions(k["emotion"])
		keywordData["keyword"] = keyword
		keywordData["relevance"] = relevance
		keywordData["emotions"] = emotions

		data["keywords"].append(keywordData)

	for e in response["entities"]:
		entityData = {}

		entity = e["text"]
		typeEntity = e["type"]
		sentiment = e["sentiment"]["label"]

		entityData["entity"] = entity
		entityData["type"] = typeEntity
		entityData["sentiment"] = sentiment

		data["entities"].append(entityData)

	# print data
	return data

def compute_top_emotions(emotionDict):
	curMax = 0
	for key, value in emotionDict.items():
		if value > curMax:
			curMax = value


	newEmotions = []
	for key, value in emotionDict.items():

		if value > .8*curMax:
			newEmotions.append(key)

	return newEmotions


if __name__ == '__main__':
    app.run(debug=True)
