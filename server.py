# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, jsonify
from model import ChangesDB

app = Flask(__name__)
debug = True
db = None

@app.route('/submit', methods=['POST'])
def submit():
    global db
    f = request.files['file']
    db = ChangesDB(f.filename)
    return jsonify({'result': 'OK'})

@app.route('/keys')
def keys():
    if db is not None:
        return jsonify({'result': db.keys().tolist()})
    else:
        return jsonify({'result': 'Error', 'msg': 'CSV file not loaded'})

@app.route('/query')
def query():
    if db is not None:
        objType = request.values.get('objType')
        objId = request.values.get('objId')
        objTime = request.values.get('objTime')
        if objType is None or objTime is None:
            return jsonify({'result': 'Error', 'msg': 'Object type and object time required'})
        else:
            return jsonify({'result': db.query(objType, objId, objTime)})
    else:
        return jsonify({'result': 'Error', 'msg': 'CSV file not loaded'})

@app.route('/')
def landing():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=debug)
