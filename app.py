from flask import Flask, request
from flask_cors import CORS

# import aws_credentials as rds
import os

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    print("hello")
    return


@app.route("/process_audio", methods=["POST"])
def process_audio():
    data = request.get_json()
    audio_file = data["audio_file"]  # should be AWS S3 link
    accident_info = data["accident_info"]

    # call AI API flow function here, gets dict accident info back

    # return accident info dict
    return
