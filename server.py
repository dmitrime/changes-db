# -*- coding: utf-8 -*-

import time
from flask import Flask, request, render_template, jsonify
from model import ChangesDB

app = Flask(__name__)
debug = True
db = None

@app.route('/submit', methods=['POST'])
def submit():
    global db
    f = request.files['file']
    try:
        db = ChangesDB(f.filename)
    except Exception as e:
        return jsonify({'result': 'Error', 'msg': e.message})

    return jsonify({'result': 'OK'})

@app.route('/keys')
def keys():
    if db is not None:
        return jsonify({'result': db.keys()})
    else:
        return jsonify({'result': 'Error', 'msg': 'CSV file not loaded'})

@app.route('/query', methods=['POST'])
def query():
    if db is not None:
        objType = None
        objId = None
        objTime = int(time.time())
        try:
            objType = request.values.get('objType')
            objTime = int(request.values.get('objTime'))
            objId = int(request.values.get('objId'))
        except:
            pass
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
