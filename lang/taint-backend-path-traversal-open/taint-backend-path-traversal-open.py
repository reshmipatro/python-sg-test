##########
# The bellow tests are from
# https://github.com/returntocorp/semgrep-rules/blob/develop/python/flask/security/injection/path-traversal-open.yaml
##########
import flask
import json

app = flask.Flask(__name__)

@app.route("/route_param/<route_param>")
def route_param(route_param):
    print("blah")
    # ruleid: taint-backend-path-traversal-open
    return open(route_param, 'r').read()

@app.route("/route_param_ok/<route_param>")
def route_param_ok(route_param):
    print("blah")
    # ok: taint-backend-path-traversal-open
    return open("this is safe", 'r').read()

@app.route("/route_param_with/<route_param>")
def route_param_with(route_param):
    print("blah")
    # ruleid: taint-backend-path-traversal-open
    with open(route_param, 'r') as fout:
        return fout.read()

@app.route("/route_param_with_ok/<route_param>")
def route_param_with_ok(route_param):
    print("blah")
    # ok: taint-backend-path-traversal-open
    with open("this is safe", 'r') as fout:
        return fout.read()

@app.route("/route_param_with_concat/<route_param>")
def route_param_with_concat(route_param):
    print("blah")
    # ruleid: taint-backend-path-traversal-open
    with open(route_param + ".csv", 'r') as fout:
        return fout.read()

@app.route("/get_param", methods=["GET"])
def get_param():
    param = flask.request.args.get("param")
    # ruleid: taint-backend-path-traversal-open
    f = open(param, 'w')
    f.write("hello world")

@app.route("/get_param_inline_concat", methods=["GET"])
def get_param_inline_concat():
    # ruleid: taint-backend-path-traversal-open
    return open("echo " + flask.request.args.get("param"), 'r').read()

@app.route("/get_param_concat", methods=["GET"])
def get_param_concat():
    param = flask.request.args.get("param")
    # ruleid: taint-backend-path-traversal-open
    return open(param + ".csv", 'r').read()

@app.route("/get_param_format", methods=["GET"])
def get_param_format():
    param = flask.request.args.get("param")
    # ruleid: taint-backend-path-traversal-open
    return open("{}.csv".format(param)).read()

@app.route("/get_param_percent_format", methods=["GET"])
def get_param_percent_format():
    param = flask.request.args.get("param")
    # ruleid: taint-backend-path-traversal-open
    return open("echo %s" % (param,), 'r').read()

@app.route("/post_param", methods=["POST"])
def post_param():
    param = flask.request.form['param']
    if True:
        # ruleid: taint-backend-path-traversal-open
        with open(param, 'r') as fin:
            data = json.load(fin)
    return data

@app.route("/post_param", methods=["POST"])
def post_param_with_inline():
    # ruleid: taint-backend-path-traversal-open
    with open(flask.request.form['param'], 'r') as fin:
        data = json.load(fin)
    return data

@app.route("/post_param", methods=["POST"])
def post_param_with_inline_concat():
    # ruleid: taint-backend-path-traversal-open
    with open(flask.request.form['param'] + '.csv', 'r') as fin:
        data = json.load(fin)
    return data

@app.route("/subexpression", methods=["POST"])
def subexpression():
    param = "{}".format(flask.request.form['param'])
    print("do things")
    # ruleid: taint-backend-path-traversal-open
    return open(param, 'r').read()

@app.route("/ok")
def ok():
    # ok: taint-backend-path-traversal-open
    open("static/path.txt", 'r')

##########
# The bellow tests are from
# https://github.com/anil-yelken/Vulnerable-Flask-App/blob/main/vulnerable-flask-app.py#L124-L134
##########
@app.route("/create_file")
def create_file():
    try:
        filename=flask.request.args.get("filename")
        text=flask.request.args.get("text")
        # ruleid: taint-backend-path-traversal-open
        file=open(filename,"w")
        file.write(text)
        file.close()
        return flask.jsonify(data="File created"), 200
    except:
        return flask.jsonify(data="File didn't create"), 200

from werkzeug.utils import secure_filename
def unsafe_with(request):
    filename = secure_filename(request.POST.get("filename"))
    # ok: taint-backend-path-traversal-open
    with open(filename, 'r') as fin:
        data = fin.read()
    return HttpResponse(data)

@app.route("/viewfile", methods=["GET"])
def viewfile():
    # Only views files in this folder
    base_dir = "/uploads"
    txt_file = flask.request.args.get("file")
    abs_path = os.path.abspath(os.path.join(txt_file, base_dir))
    if not abs_path.startswith(base_dir):
        return "Bad file path!", 400
    # ok: taint-backend-path-traversal-open
    return open(abs_path, "r").read(), 200


##########
# The bellow tests are from
# https://github.com/returntocorp/semgrep-rules/blob/develop/python/django/security/injection/path-traversal/path-traversal-open.py
##########
import re, os
from django.http import HttpResponse
from somewhere import APIView

def unsafe(request):
    filename = request.POST.get('filename')
    contents = request.POST.get('contents')
    print("something")
    # ruleid: taint-backend-path-traversal-open
    f = open(filename, 'r')
    f.write(contents)
    f.close()

def unsafe_inline(request):
    # ruleid: taint-backend-path-traversal-open
    f = open(request.GET.get('filename'))
    f.write(request.POST.get('contents'))
    f.close()

def unsafe_dict(request):
    # ruleid: taint-backend-path-traversal-open
    f = open(request.POST['filename'])
    f.write("hello")
    f.close()

def unsafe_with(request):
    filename = request.POST.get("filename")
    # ruleid: taint-backend-path-traversal-open
    with open(filename, 'r') as fin:
        data = fin.read()
    return HttpResponse(data)

def safe(request):
    filename = "/tmp/data.txt"
    # ok: taint-backend-path-traversal-open
    f = open(filename)
    f.write("hello")
    f.close()

# Real-world finding
def download_doc(request):
    url = request.GET.get("url")
    format_doc = url.split(".")
    if format_doc[-1] == "docx":
        file_name = str(int(time.time())) + ".docx"
    else:
        file_name = str(int(time.time())) + ".xlsx"

    def file_iterator(_file, chunk_size=512):
        while True:
            c = _file.read(chunk_size)
            if c:
                yield c
            else:
                break

    # ruleid: taint-backend-path-traversal-open
    _file = open(url, "rb")
    response = StreamingHttpResponse(file_iterator(_file))
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = "attachment;filename=\"{0}\"".format(file_name)
    return response

class GenerateUserAPI(APIView):
    def get(self, request):
        """
        download users excel
        """
        file_id = request.GET.get("file_id")
        if not file_id:
            return self.error("Invalid Parameter, file_id is required")
        if not re.match(r"^[a-zA-Z0-9]+$", file_id):
            return self.error("Illegal file_id")
        file_path = f"/tmp/{file_id}.xlsx"
        if not os.path.isfile(file_path):
            return self.error("File does not exist")
        # ok: taint-backend-path-traversal-open
        with open(file_path, "rb") as f:
            raw_data = f.read()
        os.remove(file_path)
        response = HttpResponse(raw_data)
        response["Content-Disposition"] = f"attachment; filename=users.xlsx"
        response["Content-Type"] = "application/xlsx"
        return response

##########
# The bellow tests are from
# https://github.com/returntocorp/semgrep-rules/blob/develop/python/django/security/injection/path-traversal/taint-backend-path-traversal-open.py
##########
from django.http import HttpResponse
import os

def foo_1(request):
  param = request.GET.get('param')
  file_path = os.path.join("MY_SECRET", param)
  # ruleid: taint-backend-path-traversal-open
  f = open(file_path, 'r')
  return HttpResponse(content=f, content_type="text/plain")

def foo_2(request):
  param = request.GET.get('param')
  file_path = os.path.join("MY_SECRET", param)
  file_path = os.path.abspath(file_path)
  # ok: taint-backend-path-traversal-open
  f = open(file_path, 'r')
  return HttpResponse(content=f, content_type="text/plain")

def user_pic(request):
    """A view that is vulnerable to malicious file access."""

    base_path = os.path.join(os.path.dirname(__file__), '../../badguys/static/images')
    filename = request.GET.get('p')

    # ruleid: taint-backend-path-traversal-open
    data = open(os.path.join(base_path, filename), 'rb').read()

    return HttpResponse(data, content_type=mimetypes.guess_type(filename)[0])
