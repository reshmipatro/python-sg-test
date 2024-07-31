import flask
import os
import shlex

app = flask.Flask(__name__)

# os.$FUNC test cases subshell cases
@app.route('insecure-ping-os')
def ping_a():
    address = flask.request.args.get("address")
    cmd = "ping -c 1 %s" % address
    # ruleid:taint-backend-os-command-injection-os
    os.popen(cmd) # Noncompliant
    # ruleid:taint-backend-os-command-injection-os
    os.popen(cmd, mode='r') # Noncompliant

# os.$FUNC test cases that open a new process (no shell injection)
@app.route('insecure-os-exec')
def ping_insecure_os_exec():
    cmd = flask.request.args.get("address")
    # ok:taint-backend-os-command-injection-os
    os.execl("/foo/bar", "/foo/bar")
    # ok:taint-backend-os-command-injection-os
    os.execv("/foo/bar", ["/foo/bar", "-a", "-b"])
    # ruleid:taint-backend-os-command-injection-os
    os.execl(cmd, cmd, "--do-smth")
    # ruleid:taint-backend-os-command-injection-os
    os.startfile(cmd, cmd, "--do-smth")
    # ruleid:taint-backend-os-command-injection-os
    os.spawnl(os.P_WAIT, cmd, "name")

# os.$FUNC test cases that open a new process (no shell injection) with shell as first arguments
@app.route('insecure-os-exec-shell')
def ping_insecure_os_exec_shell():
    cmd = flask.request.args.get("address")
    # ruleid:taint-backend-os-command-injection-os
    os.execve("/bin/bash", ["/bin/bash", "-c", cmd], os.environ)
    # ruleid:taint-backend-os-command-injection-os
    os.posix_spawnp("/bin/bash", ["/bin/bash", "-c", cmd], os.environ)
    # ruleid:taint-backend-os-command-injection-os
    os.execl("/bin/bash", "/bin/bash", "-c", cmd)
    # ruleid:taint-backend-os-command-injection-os
    os.posix_spawn("/bin/bash", "/bin/bash", "-c", cmd)
    # ruleid:taint-backend-os-command-injection-os
    os.execl("/bin/python3", "python", "-c", cmd)
    # ok:taint-backend-os-command-injection-os
    os.execl("/bin/bash", "/bin/bash", "-c", cmd2)

# os.$FUNC test cases that open a new process (no shell injection) with shell as first arguments
@app.route('insecure-os-spawn-shell')
def ping_insecure_os_exec_shell():
    cmd = flask.request.args.get("address")
    # ruleid:taint-backend-os-command-injection-os
    os.spawnve(os.P_WAIT,"/bin/bash", ["lol", "-c", cmd], os.environ)
    # ruleid:taint-backend-os-command-injection-os
    os.spawnve(os.P_WAIT,"/bin/ruby", ["lol", "-e", cmd], os.environ)
    # ruleid:taint-backend-os-command-injection-os
    os.spawnl(os.P_WAIT,"/bin/bash", "lol", "-c", cmd)
    # ok:taint-backend-os-command-injection-os
    os.spawnl(os.P_WAIT,"/bin/bash", "/bin/bash", "-c", cmd2)

@app.route('/secure-ping-os')
def ping_c():
    address = shlex.quote(flask.request.args.get("address")) # address argument is shell-escaped
    cmd = "ping -c 1 %s" % address
    # ok:taint-backend-os-command-injection-os
    os.popen(cmd), # Compliant
