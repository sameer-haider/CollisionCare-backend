import base64
import boto3
import uuid
import io
import os

# Set environment variables for AWS credentials
os.environ["AWS_ACCESS_KEY_ID"] = "AKIASDUMV4LADLS5LCWR"
os.environ["AWS_SECRET_ACCESS_KEY"] = "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"

s3 = boto3.client("s3")

# get full_report_audio from directory and encode it to base64
with open("full_report_audio.m4a", "rb") as audio_file:
    audio_bytes = audio_file.read()
    audio_base64 = base64.b64encode(audio_bytes)


def add_to_s3(audio_base64):
    bucket_name = "audio-files-hackai-utd"
    audio_base64 = audio_base64[23:]

    decoded_audio_bytes = base64.urlsafe_b64decode(audio_base64)
    reencoded_audio_data = (
        base64.urlsafe_b64encode(decoded_audio_bytes).decode("utf-8") + "=="
    )

    # Decode the audio file from Base64
    audio_bytes = base64.b64decode(reencoded_audio_data)

    # Generate a random object key
    object_key = str(uuid.uuid4())

    # Upload the file to S3
    with io.BytesIO(audio_bytes) as audio_fileobj:
        s3.upload_fileobj(audio_fileobj, bucket_name, object_key)

    # Generate a presigned URL for the uploaded file
    url = s3.generate_presigned_url(
        "get_object", Params={"Bucket": bucket_name, "Key": object_key}
    )

    return url


add_to_s3(audio_base64)
