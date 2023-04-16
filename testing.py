import base64

# Load the m4a file from disk
with open("full_report_audio.m4a", "rb") as f:
    binary_data = f.read()

# Encode the binary data as Base64
encoded_data = base64.b64encode(binary_data)

# Write the encoded data to a text file
with open("encoded_file.txt", "w") as f:
    f.write(encoded_data.decode("utf-8"))
