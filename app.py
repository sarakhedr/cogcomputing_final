from flask import Flask, render_template, request
import models

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
	print(request.data)

	#print("not yet implemented")


if __name__ == '__main__':
    app.run(port=80, debug=True)
