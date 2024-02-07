#!/usr/bin/env python3

import argparse
import csv
import json
import os
import sys

from jsonschema import validate
import yaml


def find_provenance_files(provenance_dir):
    """
    Find all provenance files in a directory.

    :param provenance_dir: Directory containing provenance files
    :type provenance_dir: str
    :return: List of provenance files
    :rtype: list[dict[str, str]]
    """
    provenance_files = []
    for root, dirs, files in os.walk(provenance_dir):
        for file in files:
            if file.endswith('.yml') or file.endswith('.yaml'):
                expected_validity = os.path.basename(file).split('_')[0]
                provenance_file = {
                    'path': os.path.join(root, file),
                    'expected_validity': expected_validity
                }
                provenance_files.append(provenance_file)

    return provenance_files


def main(args):
    schema = None
    with open(args.schema) as f:
        schema = json.load(f)

    provenance_files = find_provenance_files(args.provenance_dir)
    validation_results = []
    for provenance_file in provenance_files:
        provenance_file_path = provenance_file['path']
        provenance_file_basename = os.path.basename(provenance_file_path)
        with open(provenance_file_path) as f:
            try:
                provenance = yaml.load(f, Loader=yaml.BaseLoader)
                validate(provenance, schema)
                validation_results.append({
                    'file': provenance_file_basename,
                    'expected_validity': provenance_file['expected_validity'],
                    'actual_validity': 'valid',
                })
            except Exception as e:
                validation_results.append({
                    'file': provenance_file_basename,
                    'expected_validity': provenance_file['expected_validity'],
                    'actual_validity': 'invalid',
                })
                continue

    output_fieldnames = [
        'file',
        'expected_validity',
        'actual_validity',
    ]
    writer = csv.DictWriter(sys.stdout, fieldnames=output_fieldnames, delimiter='\t', extrasaction='ignore')
    writer.writeheader()
    for result in validation_results:
        writer.writerow(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--provenance-dir', help='Directory containing example provenance YAML files')
    parser.add_argument('-s', '--schema', help='Schema JSON file')
    args = parser.parse_args()
    main(args)

