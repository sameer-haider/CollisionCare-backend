import requests
import json
import aws_interact


def computer_accident_audio(audio_encoded, accident_info):
    audio_url = aws_interact.add_to_s3(audio_encoded)

    keys = [
        "accident_info",
        "type_severity_of_collision",
        "injuries",
        "vehicles_involved",
        "damage_to_customers_car",
        "location_of_damage",
        "witnesses",
        "police_called",
        "car_is_drivable",
    ]

    # This gets the chatgpt response of the list of requirements stored in the format below

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

                    accident_info: 
                    type_severity_of_collision:
                    injuries: 
                    vehicles_involved: 
                    damage_to_customers_car: 
                    location_of_damage: 
                    witnesses:
                    police_called:
                    car_is_drivable:
                    """,
                    "audio_input": audio_url,
                },
            }
        ),
    )

    print(response.json()["outputs"]["text_output_2"])

    # Next step is to transform the response into the requirements dictionary
    output = response.json()["outputs"]["text_output_2"]
    # print(type(output))

    # Split the string at each newline character and iterate over each line
    data_list = output.split("\n")
    for i, line in enumerate(data_list):
        # Split each line at the colon character to separate the key and value
        key, value = line.split(":")
        # Strip any whitespace from the key and value
        key = key.strip()
        value = value.strip()
        print(f"{key}--- {value}")
        if accident_info[keys[i]] is None and len(value) != 0:
            accident_info[keys[i]] = value

    print(accident_info)
