import flask
import platform

app = flask.Flask(__name__)

@app.route("platform")
def platform():
    ip = flask.request.args.get("ip")
    # ok:taint-backend-os-command-injection-platform
    platform.popen("echo 'nothing'")
    # ruleid:taint-backend-os-command-injection-platform
    platform.popen("lol" + ip)
    # ruleid:taint-backend-os-command-injection-platform
    platform.popen("lol" % ip, bla)
    # ruleid:taint-backend-os-command-injection-platform
    platform.popen(ip, bla)