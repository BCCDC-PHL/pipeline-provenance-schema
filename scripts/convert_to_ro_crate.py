#!/usr/bin/env python3

import argparse
import json
import os

from jsonschema import validate
import yaml


def collect_pipeline_metadata(provenance):
    """
    Add pipeline metadata to the RO-Crate.

    :param ro_crate: RO-Crate metadata
    :type ro_crate: dict
    :param provenance: Pipeline provenance
    :type provenance: dict
    :return: RO-Crate metadata
    :rtype: dict
    """
    pipeline_metadata = {
        "@type": ["File", "SoftwareSourceCode", "ComputationalWorkflow"],
        "programmingLanguage": {"@id": "https://w3id.org/workflowhub/workflow-ro-crate#nextflow"},
        
    }
    for provenance_record in provenance:
        if 'pipeline_name' in provenance_record:
            pipeline_name = provenance_record['pipeline_name']
            pipeline_version = provenance_record['pipeline_version']
            pipeline_metadata['@id'] = os.path.join('https://github.com', pipeline_name)
            pipeline_metadata['name'] = pipeline_name
            
            

    return pipeline_metadata


def collect_input_file_metadata(provenance):
    """
    Add input file metadata to the RO-Crate.

    :param ro_crate: RO-Crate metadata
    :type ro_crate: dict
    :param provenance: Pipeline provenance
    :type provenance: dict
    :return: RO-Crate metadata
    :rtype: dict
    """
    input_files = []
    for provenance_record in provenance:
        if 'input_filename' in provenance_record:
            input_filename = provenance_record['input_filename']
            input_file_metadata = {
                "@id": None,  # TODO: Figure out what to use here
                "@type": "FormalParameter",
                "additionalType": "File",
                "conformsTo": {
                    "@id": "https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE"
                },
                "name": input_filename,
            }
            input_files.append(input_file_metadata)

    return input_files


def main(args):
    schema = None
    provenance = None
    with open(args.schema) as f:
        schema = json.load(f)
    with open(args.provenance) as f:
        provenance = yaml.load(f, Loader=yaml.BaseLoader)

    try:
        validate(provenance, schema)
    except Exception as e:
        print(e)
        exit(1)

    ro_crate = json.load(open(args.ro_crate_template))

    pipeline_metadata = collect_pipeline_metadata(provenance)
    ro_crate['@graph'].append(pipeline_metadata)
    input_file_metadata = collect_input_file_metadata(provenance)
    ro_crate['@graph'].extend(input_file_metadata)

    print(json.dumps(ro_crate, indent=2))
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--schema', help='Schema JSON file')
    parser.add_argument('-t', '--ro-crate-template', help='RO-Crate template JSON file')
    parser.add_argument('-p', '--provenance', help='Pipeline provenance YAML file')
    args = parser.parse_args()
    main(args)
