from flask import Flask
from flask import request

from qa_retrieval import question_answer

app = Flask(__name__)


@app.route("/ping")
def ping():
    return "pong"


@app.route("/qa", methods=["POST"])
def qa():
    question = request.json["message"]
    return question_answer(question)

