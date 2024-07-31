import requests
import exec as safe_function

from flask import Flask, request

app = Flask(__name__)

@app.route("/test")
def test():
    user_input = request.args.get('cmd')
    # ruleid: taint-backend-95-dynamic-evaluation
    safe_function(user_input)

    # ruleid: taint-backend-95-dynamic-evaluation
    exec(user_input)

    # ruleid: taint-backend-95-dynamic-evaluation
    exec (user_input)

    # ruleid: taint-backend-95-dynamic-evaluation
    exec (
        user_input
    )

    # ruleid: taint-backend-95-dynamic-evaluation
    eval (
        user_input
    )

    # ok: taint-backend-95-dynamic-evaluation
    exec("ls")

    # ok: taint-backend-95-dynamic-evaluation
    some_exec(user_input)

    # ok: taint-backend-95-dynamic-evaluation
    # exec(user_input)

    # ok: taint-backend-95-dynamic-evaluation
    print("exec(bar)")

    # ok: taint-backend-95-dynamic-evaluation
    exec("x = 1; x = x + 2")

    blah = "import requests; r = requests.get('https://example.com')"
    # ok: taint-backend-95-dynamic-evaluation
    exec(blah)

    dynamic = "import requests; r = requests.get('{}')"
    # todoruleid: taint-backend-95-dynamic-evaluation
    exec(dynamic.format("https://example.com"))

    def eval_something(something):
        # todoruleid: taint-backend-95-dynamic-evaluation
        exec(something)

    from something import exec

    # ok: taint-backend-95-dynamic-evaluation
    exec("something")
