from flask import Flask, jsonify
import requests
import sys


app = Flask(__name__)


@app.route("/")
def index():
    r = requests.get("http://api-server:8001")
    print(r, file=sys.stdout)
    return r.content, r.status_code

@app.route("/hello")
def hello():
    r = requests.get("http://api-server:8001/hello")
    print(r)
    return jsonify(username="Masa"), r.status_code



if __name__ == "__main__":
    app.run(debug=True)
