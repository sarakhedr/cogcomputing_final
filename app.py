import flask

import models

app = flask.Flask(__name__)


@app.route('/api/entries', methods=['GET', 'POST'])
def api_entries():
    if flask.request.method == 'GET':
        entries = [entry.to_dict() for entry in models.Entry.select()]
        return flask.jsonify(entries)
    elif flask.request.method == 'POST':
        entry = models.Entry.create(content='Hello world')
        return flask.jsonify(entry.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
