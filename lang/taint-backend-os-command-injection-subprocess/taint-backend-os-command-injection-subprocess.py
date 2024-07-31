import flask
import subprocess
import shlex

app = flask.Flask(__name__)

# Covering subprocess with one taint argument, plus different shell modes and other flags
@app.route("first")
def first():
    ip = flask.request.args.get("ip")
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(ip)
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(ip, stdin=None)
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(ip, shell=True, stdin=None)
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(ip, shell=False)

# Covering subprocess with one taint argument, that comes after an f-string, plus different shell modes and other flags
@app.route("second")
def a():
    ip = flask.request.args.get("lolcat")
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run(f'ping {ip}')
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(f'ping {ip}', shell=True)
    # This is a fun one, if shell is set to anything
    # but False, it will be considered True
    # todoruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(f'ping {ip}', shell="lolcat")
    # Another fun one, if tainted input comes to the
    # command executable, it will be executed
    # todoruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(f'ping 127.0.0.1', executable=ip)

@app.route("second-a")
def a():
    ip = flask.request.args.get("lolcat")
    cmd = f'ping {ip}'
    # Not an issue, because it's not running as a shell
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run(cmd)
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(cmd, shell=True)

# Covering subprocess with one taint argument, that comes after a static string, plus different shell modes and other flags
@app.route("a")
def a():
    ip = flask.request.args.get("ip")
    # Not an issue, because it's not running as a shell
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip)
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, stdin=None)
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, shell=False)
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, stdin=None, shell=False)
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, stdin=None, shell=False, cwd="Bla")
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, stdin=None, cwd=False)
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, shell=True)
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip)
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(ip)
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, stdin=None, shell=True)
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, stdin=None, shell=None)
    # todoruleid:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, stdin=None, shell="None")
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, stdin=None, shell="LolcatINc")
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, stdin=None, shell="True")
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, stdin=None, shell="False")
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run("ping "+ ip, stdin=None, shell=True, cwd="bla")

# Covering subprocess with one taint argument, that comes after a static string using format, plus different shell modes and other flags
@app.route("b")
def b():
    host = flask.request.headers["HOST"]
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("echo {} > log".format(host))
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("echo {} > log".format(host), stdin=None)
    # gotta add the other args to be safe
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("echo {} > log".format(host), cwd=None)
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("echo {} > log".format(host), shell=False)
    cmd = "echo {} > log".format(host)
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run(cmd, shell=False)
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(cmd, shell=True)
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run("echo {} > log".format(host), shell=True)

# Covering subprocess with one taint argument, that comes after a static string using %, plus different shell modes and other flags
@app.route("c/<ip>")
def c(ip):
    cmd = "ping -c 1 %s" % ip
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run(cmd)
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run(cmd, shell=False)
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(cmd, cwd=None, shell=True) # Noncompliant; using shell=true is unsafe
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("ping -c 1 %s" % ip, shell=False)
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("ping -c 1 %s" % ip)
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run("ping -c 1 %s" % ip, shell=True) # Noncompliant; using shell=true is unsafe
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.Popen(cmd, shell=True) # Noncompliant; using shell=true is unsafe
    #ok:taint-backend-os-command-injection-subprocess
    subprocess.Popen(cmd)

@app.route('/insecure-sub-os')
def ping_b():
    address = flask.request.args.get("address")
    cmd = "ping -c 1 %s" % address
    # todoruleid:taint-backend-os-command-injection-subprocess
    subprocess.os.system(cmd, shell=True) # Noncompliant; using shell=true is unsafe

# Covering subprocess with a combination of taint argument being passed as an array, plus different shell modes and other flags
@app.route("d/<cmd>/<ip>")
def d(cmd, ip):
    command = [cmd, ip]
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.check_output(command)

@app.route("e")
def e():
    event = flask.request.json
    cmd = event['id'].split()
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.call([cmd[0], cmd[1], "some", "args"])
    
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.call((cmd[0], cmd[1], "some", "args"))

@app.route("f")
def f():
    event = flask.request.get_json()
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(["bash", "-c", event['id']], shell=True)
    # ruleid:taint-backend-os-command-injection-subprocess
    subprocess.run(("bash", "-c", event['id']), shell=True)

@app.route("d_ok/<cmd>/<ip>")
def d_ok(cmd, ip):
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.check_output(["ping", cmd, ip])

@app.route("d_ok2/<ip>")
def d_ok2(ip):
    cmd = ["ping", ip]
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.check_output(cmd)

@app.route("e")
def e_ok():
    allowed = {'p': "ping"}

    event = flask.request.json
    cmd = event['id'].split()

    valid = allowed[cmd[0]]
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.call([valid, "some", "args"])

@app.route("ok")
def ok():
    ip = flask.request.args.get("ip")
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run(["ping", ip])

@app.route("ok3")
def ok3():
    ip = flask.request.args.get("ip")
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.call(["echo", "a", ";", "rm", "-rf", "/"])

@app.route('/secure-ping-sub')
def ping_d():
    address = flask.request.args.get("address")
    args = ["ping", "-c1", address]
    #ok:taint-backend-os-command-injection-subprocess
    subprocess.Popen(args) # Compliant


# Covering an interpreter as the command followed by tainted input
@app.route("g")
def g():
    event = flask.request.json

    # ruleid:taint-backend-os-command-injection-subprocess
    program = subprocess.Popen(['python2', event], stdin=subprocess.PIPE, text=True)
    # ruleid:taint-backend-os-command-injection-subprocess
    program = subprocess.run(['python3', "-c", event['id']], stdin=subprocess.PIPE, text=True)
    # ruleid:taint-backend-os-command-injection-subprocess
    program = subprocess.run(['ruby', "-e", event['id']], stdin=subprocess.PIPE, text=True)
    program.communicate(input=payload, timeout=1)

@app.route('/secure-ping-sanitized')
def ping_sc():
    address = shlex.quote(flask.request.args.get("address")) # address argument is shell-escaped
    #ok:taint-backend-os-command-injection-subprocess
    subprocess.call(address, shell=True) # Compliant
    #ok:taint-backend-os-command-injection-subprocess
    subprocess.call(address, shell=False) # Compliant

# simple static string
@app.route("ok2")
def ok2():
    ip = flask.request.args.get("ip")
    # ok:taint-backend-os-command-injection-subprocess
    subprocess.run("echo 'nothing'")
