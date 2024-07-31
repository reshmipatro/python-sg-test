import flask
import popen2

app = flask.Flask(__name__)

# simple static string
@app.route("popen2")
def popen2():
    ip = flask.request.args.get("ip")
    # ok:taint-backend-os-command-injection-popen2
    popen2.popen2("echo 'nothing'")
    # ruleid:taint-backend-os-command-injection-popen2
    popen2.popen3("lol" + ip)
    # ruleid:taint-backend-os-command-injection-popen2
    popen2.Popen4("lol" % ip, bla)
    # ruleid:taint-backend-os-command-injection-popen2
    popen2.Popen3(ip, bla)