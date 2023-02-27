import yaml
import json

## Read the YAML file
with open("wikimedia-rest-api.yaml") as infile:
    doc = yaml.load(infile.read())
    with open("wikimedia-rest-api.json", 'w') as outfile:
        json.dump(doc,outfile,indent=2)
