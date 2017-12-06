from flask import Flask, render_template, request
import models
import requests

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
    	'Content-Type': 'audio/flac',
	}

	data = request.data#open('audio-file.flac', 'rb').read()

	response = requests.post('https://stream.watsonplatform.net/speech-to-text/api/v1/recognize', headers=headers, data=data, auth=('9cd8ec3d-2d11-4884-8f07-fb4ed37c2add', 'Y33pRZN5DizL'))
	print(reponse.text)
	print("Response Status: " + str(response.status_code))

if __name__ == '__main__':
    app.run(port=80, debug=True)
