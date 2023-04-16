from flask import Flask, request
from flask_cors import CORS
import computing
import os
import requests
import json
from flask import Flask, jsonify

keys = ['accident_info', 'type_severity_of_collision', 'injuries', 'vehicles_involved', 'damage_to_customers_car', 'location_of_damage', 'witnesses', 'police_called', 'car_is_drivable']
requirements = {
    'accident_info': None,
    'type_severity_of_collision': None,
    'injuries' : None,
    'vehicles_involved' : None,
    'damage_to_customers_car' : None,
    'location_of_damage' : None,
    'witnesses' : None,
    'police_called' : None,
    'car_is_drivable' : None,

}

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
    accident_info = computing.get_accident_info(audio_file, accident_info)

    # return accident info dict
    return 202, accident_info
