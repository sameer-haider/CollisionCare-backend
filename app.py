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
