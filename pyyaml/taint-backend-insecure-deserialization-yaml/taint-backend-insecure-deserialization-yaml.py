# example from https://medium.com/gdg-vit/deserialization-attacks-d312fbe58e7d


from flask import Flask, make_response, request
from base64 import b64encode, b64decode
import yaml

# The main Flask Backend
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    user_obj = request.cookies.get('uuid')
    # ruleid:taint-backend-insecure-deserialization-yaml
    return "Hey there! {}!".format(yaml.unsafe_load(user_obj))

@app.route('/a', methods=['GET'])
def a():
    user_obj = request.cookies.get('uuid')
    # ruleid:taint-backend-insecure-deserialization-yaml
    return "Hey there! {}!".format(yaml.load(user_obj, Loader=yaml.Loader))

@app.route('/b', methods=['GET'])
def b():
    user_obj = request.cookies.get('uuid')
    # ruleid:taint-backend-insecure-deserialization-yaml
    return "Hey there! {}!".format(yaml.load(user_obj, Loader=yaml.CLoader))

@app.route('/c', methods=['GET'])
def c():
    user_obj = request.cookies.get('uuid')
    # ruleid:taint-backend-insecure-deserialization-yaml
    return "Hey there! {}!".format(yaml.load_all(user_obj, Loader=yaml.UnsafeLoader))
    

@app.route('/d', methods=['GET'])
def d():
    user_obj = request.cookies.get('uuid')
    # ruleid:taint-backend-insecure-deserialization-yaml
    return "Hey there! {}!".format(yaml.load_all(user_obj, Loader=yaml.CLoader))

@app.route('/e', methods=['GET'])
def e():
    user_obj = request.cookies.get('uuid')
    # ok:taint-backend-insecure-deserialization-yaml
    return "Hey there! {}!".format(yaml.load_all(user_obj, Loader=yaml.SafeLoader))

@app.route('/f', methods=['GET'])
def f():
    user_obj = request.cookies.get('uuid')
    # ok:taint-backend-insecure-deserialization-yaml
    return "Hey there! {}!".format(yaml.load_all(user_obj, Loader=yaml.CSafeLoader))

def check_ruamel_yaml():
    from ruamel.yaml import YAML
    yaml = YAML(typ="rt")
    # ok:taint-backend-insecure-deserialization-yaml
    yaml.load("thing.yaml")
    # ok:taint-backend-insecure-deserialization-yaml
    yaml.load_all("thing.yaml")


@app.route('/yaml')
def yaml_load():
    # This is a fun one, it looks insecure, but it's using the wrong taint source (e.g django, which is not imported).
    # This rule is a good example that our taint sources are working as expected.
    # ok:taint-backend-insecure-deserialization-yaml
    data = request.GET.get("data")
    yaml.load(data, Loader=yaml.Loader) # Noncompliant; Avoid using yaml.load with unsafe yaml.Loader
