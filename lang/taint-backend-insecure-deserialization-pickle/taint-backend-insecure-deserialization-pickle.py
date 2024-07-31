import pickle
import _pickle
import cPickle
import base64

from flask import Flask, request

app = Flask(__name__)


@app.route("/deser-pickle")
def deser_pickle():
    # ruleid: taint-backend-insecure-deserialization-pickle
    pickle.load(request.files['pickle'].stream)
    # ruleid: taint-backend-insecure-deserialization-pickle
    _pickle.load(request.files['pickle'].stream)
    # ruleid: taint-backend-insecure-deserialization-pickle
    cPickle.load(request.files['pickle'].stream)
    # ruleid: taint-backend-insecure-deserialization-pickle
    pickle.loads(base64.b64decode(request.args["pickle"]))
    # ruleid: taint-backend-insecure-deserialization-pickle
    _pickle.loads(base64.b64decode(request.args["pickle"]))
    # ruleid: taint-backend-insecure-deserialization-pickle
    cPickle.loads(base64.b64decode(request.args["pickle"]))
    # ok: taint-backend-insecure-deserialization-pickle
    pickle.loads(pickle.dumps({1: [1,2,34]}), encoding=request.args["encoding"])
    # ok: taint-backend-insecure-deserialization-pickle
    pickle.load("test.pickle", encoding=request.args["encoding"])
    # ok: taint-backend-insecure-deserialization-pickle
    _pickle.loads(pickle.dumps({1: [1,2,34]}), encoding=request.args["encoding"])
    # ok: taint-backend-insecure-deserialization-pickle
    _pickle.load("test.pickle", encoding=request.args["encoding"])
    # ok: taint-backend-insecure-deserialization-pickle
    cPickle.loads(pickle.dumps({1: [1,2,34]}), encoding=request.args["encoding"])
    # ok: taint-backend-insecure-deserialization-pickle
    cPickle.load("test.pickle", encoding=request.args["encoding"])
