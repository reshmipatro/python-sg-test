import flask
import commands

app = flask.Flask(__name__)

@app.route("commands")
def commands():
    ip = flask.request.args.get("ip")
    # ok:taint-backend-os-command-injection-commands
    commands.getoutput("echo 'nothing'")
    # ruleid:taint-backend-os-command-injection-commands
    commands.getoutput("lol" + ip)
    # ruleid:taint-backend-os-command-injection-commands
    commands.getoutput("lol" % ip, bla)
    # ruleid:taint-backend-os-command-injection-commands
    commands.getoutput(ip, bla)