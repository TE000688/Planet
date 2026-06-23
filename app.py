"""Planet App – Flask web application with chatbot."""

from flask import Flask, render_template, request, jsonify
from chatbot import get_response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = str(data.get("message", "")).strip()
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    reply = get_response(user_message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    import os
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")
