#!/usr/bin/env python3

import argparse
import json

from jsonschema import validate
import yaml

def main(args):
    schema = None
    with open(args.schema) as f:
        schema = json.load(f)
    with open(args.provenance) as f:
        provenance = yaml.load(f, Loader=yaml.BaseLoader)

    try:
        validate(provenance, schema)
        print('Provenance file is valid')
    except Exception as e:
        print(e)
        exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--provenance', help='Pipeline YAML file')
    parser.add_argument('-s', '--schema', help='Schema JSON file')
    args = parser.parse_args()
    main(args)

