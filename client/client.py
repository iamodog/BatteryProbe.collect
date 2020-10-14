#!/opt/batteryprobe/probe_env/bin/python3

"""Main client script.

Collect the data from a bash script, and send it to a remote database along 
with some additional elements.
"""


import os
import sys
import logging
import argparse
from uuid import uuid4
from time import sleep 
from pathlib import Path
from os.path import isfile, isdir, join

import requests
import subprocess
import daemon 


CACHE_DIR = join(str(Path.home()), ".battery_probe")
CACHE_FILE = "uuid"
SEPARATOR = ":"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--interval",
    default=10,
    help="Data scrapping frequency (in seconds)"
)
parser.add_argument(
    "--database_uri",
    default="localhost:8086",
    help="[ip]:[port]", 
)
parser.add_argument(
    "--linux",
    action="store_true"
)
parser.add_argument(
    "--mac_os",
    action="store_true"
)
parser.add_argument(
    "--debug",
    action="store_true"
)


def client():
    """Run scraping script and send output to remote database"""
    # Run OS-specific scraping script
    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE
    )
   
    # Format output 
    if result.returncode == 0:
        payload = format_payload(result.stdout.decode("utf-8"))
    else:
        logging.error("Bash script failed to scrap data")
        sys.exit(1) 
    logging.debug(payload)
    # Send payload
    try:
        response = requests.post(
            f"http://{args.database_uri}/write?db=monitoring&precision=s",
            headers={"Content-type": "text/xml"}, 
            data=payload,
        )
        if 400 <= response.status_code < 500:
            logging.error(f"InfluxDB could not understand the request. \
                Response: {response.json()}"
            )
            sys.exit(1)
        elif 500 <= response.status_code:
            logging.error(f"The system is overloaded or significantly impaired. \
                Response: {response.json()}"
            )
            sys.exit(1)
    except requests.exceptions.ConnectionError as err:
        logging.error("Request failed. DB server may be down.")
        sys.exit(1)


def get_uuid():
    """Return an universally unique ID to identify the host machine"""
    # If uuid already exists
    if isfile(join(CACHE_DIR, CACHE_FILE)):
        with open(join(CACHE_DIR, CACHE_FILE), "r") as file:
            return file.read()
    # If not, create one
    else:
        if not isdir(CACHE_DIR):
            os.mkdir(CACHE_DIR)
        with open(join(CACHE_DIR, CACHE_FILE), "a") as file:
            uuid = str(uuid4()).replace("-", "")
            file.write(uuid)
            return uuid


def format_payload(data):
    """Format the bash script output into an URL-encoded payload.

    InfluxDB API docs: 
        https://docs.influxdata.com/influxdb/v1.8/guides/write_data/

    Args:
        data (str): Measurements and their values (comma separated). 
            A tag is identified by a '@'. Tags are applied globally to 
            every measurement.
    
    Returns: 
        Payload (str) with the following format:
        [measurement],[tag=,tag=,...] [field]=[value] [epoch]
    """
    # Parse str to dict 
    data = {
        el.split(SEPARATOR)[0]: el.split(SEPARATOR)[1] 
        for el in data.split("\n") 
        if len(el) != 0 and el.split(SEPARATOR)[1] != "" 
    }

    # Extract epoch
    epoch = data["epoch"]
    del data["epoch"]

    # Extract tags
    tags = {
        key[1:]: value 
        for key, value in data.items() if key.startswith("@")
    }
    if len(tags) == 0:
        logging.error("No tags found")
        sys.exit(1)
    for key in tags:
        del data["@"+key]
    # Additional tags
    tags["os"] = "linux" if args.linux else "macos"
    tags["uuid"] = uuid

    # Format the payload 
    payload = ""
    for measurement, value_m in data.items():
        payload += f"{measurement}"
        for tag, value_t in tags.items():
            payload += f",{tag}={value_t}"
        payload += f" value={value_m} {epoch}\n"  
    return payload


def main():
    global uuid, command
    uuid = get_uuid()
    if args.mac_os:
        command = "../scrap/MACOS/scrap.sh"
    elif args.linux:
        command = "../scrap/Linux/scrap.sh"
    else:
        raise AssertionError("OS not specified")
    while True:
        client()
        sleep(int(args.interval))

if __name__ == "__main__":
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    dir_path = os.path.dirname(os.path.realpath(__file__)) ## Get the directory path of the file
    error_logs_file = open(dir_path+'/../logs/error_logs.txt','a')
    context = daemon.DaemonContext(
        working_directory = dir_path,
        stderr = error_logs_file
        )
    with context:
        main()
