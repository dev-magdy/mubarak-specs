import argparse
import sys
import requests
import json
import os
import subprocess
from yaml import load, dump

parser = argparse.ArgumentParser(description='Check compliance and optionally test endpoints. Requires python packages: pyyaml, requests and schemathesis')
parser.add_argument('--filename', type=str, required=True,
                    help='JSON or YAML filename or url')
parser.add_argument('--test-schema', type=bool, default=True,
                    help='test schema endpoints with schemathesis. Default is true')
parser.add_argument('--assert-example', type=bool, default=True,
                    help='check that each operation has an example. Default is true.')
parser.add_argument('--assert-operationid', type=bool, default=True,
                    help='check that each operation has an Id in camel case. Default is true.')

args = parser.parse_args()

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def get_file(url):
    response=requests.get(url)
    if response.ok:
        contents=response.content
        return contents
    raise Exception(f"Unable to fetch file using url {url}")

def load_file(filename):
    if filename.endswith("yaml") or filename.endswith("yml"):
        if filename.startswith("http"):
            return load(get_file(filename),Loader=Loader)
        return load(open(filename,"r"),Loader=Loader)
    if filename.endswith("json"):
        if filename.startswith("http"):
            return json.loads(get_file(filename),Loader=Loader)
        return json.load(open(filename,"r"))
    raise Exception("file name does not end with yaml,yml or json")

filename = args.filename



obj = load_file(filename)

verbs=["get"]
for path in obj["paths"]:
    path_obj = obj["paths"][path]
    if not path_obj:
        continue
    for verb in verbs:
        if verb in path_obj:
            if 'parameter' in path_obj[verb]:
                for parameter in path_obj[verb]['parameters']:
                    if args.assert_example:
                        assert "example" in parameter, f"example property not in {path} {verb}.{parameter['name']}"
                    if args.assert_operationid:
                        assert "operationId" in parameter, f"operationId property not in {path} {verb}.{parameter['name']}"
                        operationId = parameter['name']
                        assert "_" in operationId or "-" in operationId or " " in operationId,f"operationId property is not in camelCase and contains space, - or _ in {path} {verb}.{parameter['name']}"
                        
                    
if args.test_schema:
    server = obj["servers"][0]["url"]
    p = subprocess.run(f"st run {filename} --base-url={server} --checks=all --junit-xml=test_report.xml",shell=True)

    

