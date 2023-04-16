import boto3
import json
import requests
import os



# add to s3 bucket
def upload_to_s3(file_name, bucket, object_name=None):
    #
