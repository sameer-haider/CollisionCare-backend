from flask import Flask, request
from flask_cors import CORS
import computing
import os
import requests
import json
from flask import Flask, jsonify
import mysql.connector
from models import CollisionReport
import uuid
import random
from generate_email import generate_email

app = Flask(__name__)
CORS(app)

rand_gen = random.Random()

INSURANCE_ID = 210002
NAME = "Henry Freud"
ADDRESS = "2305 West Fairview Lane, Allen, TX, 75093"


app.config["MYSQL_HOST"] = os.environ.get("DATABASE_HOST")
app.config["MYSQL_USER"] = os.environ.get("DATABASE_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("DATABASE_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("DATABASE_NAME")


@app.route("/")
def index():
    print("hello")
    return "hello"


@app.route("/process_audio", methods=["POST"])
def process_audio():
    data = request.get_json()
    print(data)
    accident_info = data["accident_info"]
    audio_file = data.get("audio_file")  # should be AWS S3 link

    # call AI API flow function here, gets dict accident info back
    accident_info = computing.update_accident_info(audio_file, accident_info)

    result = {"accident_info": accident_info}
    # return accident info dict
    return jsonify(result), 202


# get claim info to display on the geico employee view
@app.route("/get_report/<int:insurance_id>", methods=["GET"])
def get_report(insurance_id):
    db = mysql.connector.connect(
        host=os.environ.get("DATABASE_HOST"),
        user=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD"),
        database=os.environ.get("DATABASE_NAME"),
    )
    columns = [
        "report_id",
        "insurance_id",
        "type_severity_of_collision",
        "injuries",
        "vehicles_involved",
        "damage_to_customers_car",
        "location_of_damage",
        "witnesses",
        "police_called",
        "car_is_drivable",
    ]
    query = f"SELECT * FROM claims_history WHERE insurance_id = {insurance_id}"
    cur = db.cursor()
    cur.execute(query)
    sql_answers = cur.fetchall()

    fin_reports = []
    for row in sql_answers:
        reports = {}
        for i in range(len(columns)):
            reports[columns[i]] = row[i]
        fin_reports.append(reports)

    return jsonify(fin_reports), 200


# Front end needs to send data in the format:
# "type_severity_of_collision",
# "injuries",
# "vehicles_involved",
# "damage_to_customers_car",
# "location_of_damage",
# "witnesses",
# "police_called",
# "car_is_drivable"


@app.route("/submit_report", methods=["POST"])
def submit_report():
    db = mysql.connector.connect(
        host=os.environ.get("DATABASE_HOST"),
        user=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD"),
        database=os.environ.get("DATABASE_NAME"),
    )
    data = request.get_json()
    report_id = generate_uid()
    report_values = (
        INSURANCE_ID,
        data["type_severity_of_collision"],
        data["injuries"],
        data["vehicles_involved"],
        data["damage_to_customers_car"],
        data["location_of_damage"],
        data["witnesses"],
        data["police_called"],
        data["car_is_drivable"],
    )
    query = "INSERT INTO claims_history (insurance_id, type_severity_of_collision, injuries, vehicles_involved, damage_to_customers_car, location_of_damage, witnesses, police_called, car_is_drivable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur = db.cursor()
    cur.execute(query, report_values)
    db.commit()
    return "Success", 200


def generate_uid():
    return random.randint(100000, 999999)


@app.route("/get_email/<int:insurance_id>", methods=["GET"])
def email(insurance_id):
    columns = [
        "report_id",
        "insurance_id",
        "type_severity_of_collision",
        "injuries",
        "vehicles_involved",
        "damage_to_customers_car",
        "location_of_damage",
        "witnesses",
        "police_called",
        "car_is_drivable",
    ]
    db = mysql.connector.connect(
        host=os.environ.get("DATABASE_HOST"),
        user=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD"),
        database=os.environ.get("DATABASE_NAME"),
    )
    query = f"SELECT * FROM claims_history WHERE insurance_id = {insurance_id} ORDER BY report_id DESC LIMIT 1;"
    cur = db.cursor()
    cur.execute(query)
    sql_answers = cur.fetchall()

    fin_reports = []
    for row in sql_answers:
        reports = {}
        for i in range(len(columns)):
            reports[columns[i]] = row[i]
        fin_reports.append(reports)
    # print(fin_reports)
    values = (
        fin_reports[0]["type_severity_of_collision"],
        fin_reports[0]["location_of_damage"],
        fin_reports[0]["car_is_drivable"],
    )
    print(values)
    response = generate_email(
        f"Severity of damage - {values[0]}, location of damage - {values[1]}, is the car drivable? - {values[2]}"
    )
    return response
