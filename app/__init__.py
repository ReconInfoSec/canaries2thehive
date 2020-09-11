from __future__ import print_function
from __future__ import unicode_literals

import sys
import requests
import json
import os
import time
import uuid
import logging
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper
from flask import Flask, Response, request, flash, redirect, url_for
from config import Config


app = Flask(__name__)
app.config.from_object(Config)


def flatten_dict(d):
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    yield subkey, subvalue
            else:
                yield key, value

    return dict(items())


@app.route('/create_alert', methods=['POST'])
def create_alert():

    # Get request data
    content = request.get_json()

    # Configure logging
    logging.basicConfig(filename=app.config['LOG_FILE'], filemode='a',
                        format='%(asctime)s - canaries2thehive - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logging.info(json.dumps(content))

    # Configure artifacts
    artifacts = []
    artifacts.append(AlertArtifact(dataType='ip',
                                   tags=[],
                                   data=content['CanaryIP']))
    artifacts.append(AlertArtifact(dataType='ip',
                                   tags=[],
                                   data=content['SourceIP']))
    artifacts.append(AlertArtifact(dataType='fqdn',
                                   tags=[],
                                   data=content['CanaryName']))

    # Tags list
    tags = ['canary']

    # Parse fields and create description
    description = ""
    alert_flattened = flatten_dict(content)
    for key in alert_flattened.keys():
        if (alert_flattened[key] != ""):
            description = description+"\n**"+key+":** "+json.dumps(alert_flattened[key])+"\n"

    # Prepare alert
    sourceRef = str(uuid.uuid4())[0:6]
    alert = Alert(title="Canary Triggered - %s by %s on %s (%s)" % (content["Description"], content["SourceIP"], content["CanaryName"], content["CanaryIP"]),
                  tlp=2,
                  tags=tags,
                  description=description,
                  type='external',
                  source='canary',
                  artifacts=artifacts,
                  sourceRef=sourceRef)

    # Get API keys
    with open(app.root_path + '/keys.json', 'r') as file:
        keys_file = file.read()
    keys = json.loads(keys_file)

    # Loop through organisations in TheHive
    for org, key in keys.items():

        # Configure API
        logging.info(app.config['HIVE_URL'])
        api = TheHiveApi(app.config['HIVE_URL'], key)

        # Create the alert
        logging.info('Create Alert')
        logging.info('-----------------------------')
        id = None
        response = api.create_alert(alert)
        if response.status_code == 201:
            logging.info(json.dumps(response.json(), indent=4, sort_keys=True))
            id = response.json()['id']
        else:
            logging.info('ko: {}/{}'.format(response.status_code,
                                            response.text))
            sys.exit(0)

        # Return
        return "Hive Alert Created"
