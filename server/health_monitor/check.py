"""A sys admin should be the first person to know that a service is down.

This is to make sure you do.
There is probably a better way to do it. Something alredy built for this.
"""


import json
import logging
import argparse
from time import sleep
from os.path import isfile
from datetime import datetime

import requests


parser = argparse.ArgumentParser()
parser.add_argument("--params", default="")


def is_healthy():
    """Check if remote db is healthy."""
    response = requests.get(f"http://{params['db_uri']}/health")
    return response.json()["status"] == "pass"


def unhealthy_state():
    """Define the unhealthy state behavior."""
    logging.info(
        "Entered unhealthy state at %s",
        datetime.now().strftime("%H:%M:%S")
    )
    discord_alert(False)
    while not is_healthy():
        logging.info(
            "Checking again in %s min",
            params["unhealthy_check_interval"]
        )
        sleep(params["unhealthy_check_interval"] * 60)
    logging.info(
        "Healthy again at %s",
        datetime.now().strftime("%H:%M:%S")
    )
    discord_alert(True)
    return


def discord_alert(is_healthy):
    """Send an alert on discord using webhooks."""
    now = datetime.now().strftime("%H:%M:%S")
    if is_healthy:
        data = {"content": f"Service is back on ! @{now}"}
    else:
        data = {"content": f"@everyone SERVICE IS DOWN ! @{now}"}

    requests.post(
        params["db_uri"],
        data=json.dumps(data),
        headers={"Content-Type": "application/json"}
    )


if __name__ == "__main__":
    args = parser.parse_args()
    assert isfile(args.params), "No parameters file found."
    logging.basicConfig(level=logging.INFO)
    params = json.load(open(args.params, "r"))
    while True:
        if is_healthy():
            logging.info(
                "Healthy. Checking again in %s min",
                params["healthy_check_interval"]
            )
            sleep(params["healthy_check_interval"] * 60)
        else:
            unhealthy_state()
