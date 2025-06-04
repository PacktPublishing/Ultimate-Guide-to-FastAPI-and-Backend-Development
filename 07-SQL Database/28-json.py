import json


shipments = {}


### Load from .json file
with open("shipments.json") as json_file:
    data = json.load(json_file)

    # Map as dictionary
    for value in data:
        shipments[value["id"]] = value


### Save changes to .json file
def save():
    with open("shipments.json", "w") as json_file:
        json.dump(
            # Convert to list of shipments
            list(shipments.values()),
            json_file,
        )