from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    raise

# ruleid: 215-debug
app.run(debug=True)

# ok: 215-debug
app.run()
# ok: 215-debug
app.run(debug=False)

# ok: 215-debug
run()
# ok: 215-debug
run(debug=True)
# ok: 215-debug
run(debug)