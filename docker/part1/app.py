from flask import Flask

app = Flask(__name__)

@app.route('/')
def startpage():
    return "Home"

@app.route('/healthcheck')
def healthcheck():
    return '{"status":"ok"}'

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000)