from flask import Flask
from flask_cors import CORS

# import aws_credentials as rds
import os

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    print("hello")
    return


@app.route("process_audio", methods=["POST"])
def process_audio():
    print("hello")
    return
