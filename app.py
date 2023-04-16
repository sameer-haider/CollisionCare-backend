from flask import Flask, request
from flask_cors import CORS
import computing
import os
import requests
import json
from flask import Flask, jsonify


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    print("hello")
    return "hello"


@app.route("/process_audio", methods=["POST"])
def process_audio():
    data = request.get_json()
    audio_file = data["audio_file"]  # should be AWS S3 link
    accident_info = data["accident_info"]

    # call AI API flow function here, gets dict accident info back
    accident_info = computing.update_accident_info(audio_file, accident_info)

    result = {"accident_info": accident_info}
    # return accident info dict
    return jsonify(result), 202
