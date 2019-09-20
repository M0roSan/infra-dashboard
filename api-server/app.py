from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(username="Masa"), 200


@app.route("/hello")
def hello():
    return jsonify(foo="bar",
                   username="Masa"), 200


if __name__ == "__main__":
    app.run(debug=True)
