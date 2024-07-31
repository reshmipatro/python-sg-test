import paramiko
from flask import Flask
app = Flask(__name__)


def sanitize(input):
    return input[1:2]


client = paramiko.client.SSHClient()
lol = "cat"

if __name__ == '__main__':
    app.add_url_rule('/user/<user_id>', view_func=get_user)

    add_a_route(app)
    add_a_route_with_decorator(app)
    add_a_route_with_blueprint(global_bp)
    
    app.run(debug= True)


@app.route('/blog/page/<arg>')
def get_command_arg(arg):
    # ruleid: taint-backend-78-sshclient-exec_command
    client.exec_command(arg)

    # ruleid: taint-backend-78-sshclient-exec_command
    client.exec_command('ls ' + arg)

    # todook: taint-backend-78-sshclient-exec_command
    client.exec_command(sanitize(arg))

    # todook: taint-backend-78-sshclient-exec_command
    client.exec_command('ls ' + sanitize(arg))

    # ok: taint-backend-78-sshclient-exec_command
    client.exec_command(lol)

    # ok: taint-backend-78-sshclient-exec_command
    client.exec_command('plain string')

    # ok: taint-backend-78-sshclient-exec_command
    client.connect('somehost')

    return "Same arg"
