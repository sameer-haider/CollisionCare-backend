import requests
import json


severity = False
injuries = False
vehicles = False
damage = False
location = False
witnesses = False
police = False
car = False


response = requests.post(
    "https://api.respell.ai/v1/run",
    headers={
        # This is your API key
        "Authorization": "Bearer 2e116ae5-8787-491e-9b50-8ea34e4d31a6",
        "Accept": "application/json",
        "Content-Type": "application/json",
    },
    data=json.dumps(
        {
            "spellId": "Mf0I-6b0sGTN_4nf4KJZ2",
            # Fill in dynamic values for each of your 2 input blocks
            "inputs": {
                "instructions": """The message will be a transcript of a insurance customer who is giving various details about their car crash that just happened. The information will not all be there, but try to format all the info into a bullet point format that an insurance agent can later read and process. If there is some information missing like location of dent in car etc., put that in the bullet list but leave the entry empty.

                        - Type/Severity of collision: 
                        - Injuries: 
                        - Vehicles Involved:
                        - Damage to customer's car: 
                        - Location of damage: 
                        - Witnesses: 
                        - Police called: 
                        - Car is drivable:""",
                "audio_input": "https://audio-files-hackai-utd.s3.amazonaws.com/full_report_audio.m4a",
            },
        }
    ),
)


print(response)

output = response.json()["outputs"]["text_output_2"]
print(output)

response = requests.post(
    "https://api.respell.ai/v1/run",
    headers={
        # This is your API key
        "Authorization": "Bearer 2e116ae5-8787-491e-9b50-8ea34e4d31a6",
        "Accept": "application/json",
        "Content-Type": "application/json",
    },
    data=json.dumps(
        {
            "spellId": "VidUxREA-ozloE_ARul-f",
            # This field can be omitted to run the latest published version
            "spellVersionId": "xuPf7RhiqxP2ZzvwdjQ-e",
            # Fill in dynamic values for each of your 2 input blocks
            "inputs": {
                "instruction": "Given the current list of items, please put them in JSON format",
                "formatted_info": output,
            },
        }
    ),
)

print(response)

output = response.json()["outputs"]["text_output"]
print(output)
