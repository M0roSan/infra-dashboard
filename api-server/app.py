from flask import Flask, render_template, jsonify


application = Flask(__name__)

@application.route("/")
def index():
    return render_template("index.html")

@application.route("/hello")
def hello():
    return jsonify(foo="bar",
                   username="Masa"), 200


if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0")
