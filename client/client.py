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

import daemon 
import requests
import subprocess
from daemon import pidfile


CACHE_DIR = join(str(Path.home()), ".battery_probe")
UUID_FILE = "uuid"
QUEUE_FILE = "queue"
MAX_QUEUE_FILE_SIZE = 5000000
SEPARATOR = ":"
PID_FILE="/var/run/battery_probe.pid"

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
        send_payload(payload)        
    except requests.exceptions.ConnectionError as err:
        logging.error("Request failed. DB server may be down.")
        logging.info("Adding payload to queue")
        # If server can't be reached, the payload is kept in cache
        # to be sent later.
        cache_payload(payload)
               

def cache_payload(payload):
    """Add payload to cache."""
    queue_path = join(CACHE_DIR, QUEUE_FILE)
    try:
        file_size = os.path.getsize(queue_path)
    except FileNotFoundError:
        file_size = 0
    if file_size < MAX_QUEUE_FILE_SIZE:
        with open(queue_path, "ab") as queue_file:
                queue_file.write((payload + "\0").encode())
    else:
        logging.info("Queue file size exceed the limit fixed to 5mb. Following data will not be save.")


def db_is_reachable():
    """Check if database is reachable."""
    try:
        response = requests.get(f"http://{args.database_uri}/ping")
        logging.debug("DB is reachable")
        return response.status_code == 204
    except requests.exceptions.ConnectionError as err:
        return False


def send_payload(payload):
    response = requests.post(
        f"http://{args.database_uri}/write?db=monitoring&precision=s",
        headers={"Content-type": "text/xml"}, 
        data=payload,
    )
    if 400 <= response.status_code < 500:
        logging.error(f"InfluxDB could not understand the request. \
            Response: {response.json()}"
        )
    elif 500 <= response.status_code:
        logging.error(f"The system is overloaded or significantly impaired. \
            Response: {response.json()}"
        )
 

def get_uuid():
    """Return an universally unique ID to identify the host machine"""
    # If uuid already exists
    if isfile(join(CACHE_DIR, UUID_FILE)):
        with open(join(CACHE_DIR, UUID_FILE), "r") as file:
            return file.read()
    # If not, create one
    else:
        if not isdir(CACHE_DIR):
            os.mkdir(CACHE_DIR)
        with open(join(CACHE_DIR, UUID_FILE), "a") as file:
            uuid = str(uuid4()).replace("-", "")
            file.write(uuid)
            return uuid


def send_cached_payloads():
    # If queue is not empty and DB is reachable
    if isfile(join(CACHE_DIR, QUEUE_FILE)) and db_is_reachable():
        logging.info("Sending cached payloads to remote DB")
        queue_file = open(join(CACHE_DIR, QUEUE_FILE), "rb")
        
        # Put payloads in a python list
        payloads = queue_file.read().decode("utf-8")
        payloads = payloads.split("\0")
        
        # Delete queue file
        queue_file.close()
        logging.debug("Removing queue file from cache")
        os.remove(join(CACHE_DIR, QUEUE_FILE))

        while len(payloads) != 0:
            # FIFO access
            payload = payloads.pop(0)
            try:
                send_payload(payload)
            except requests.exceptions.ConnectionError as err:
                # If an error occurs at this stage we put the remaining
                # payloads back in cache
                cache_payload(payload)
                for payload in payloads:
                    cache_payload(payload)


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

def select_os(args):
    if args.mac_os:
        command = "../scrap/MACOS/scrap.sh"
    elif args.linux:
        command = "../scrap/UNIX/scrap.sh"
    else:
        raise AssertionError("OS not specified")
    return command #inutile car command est global

def select_logging_mode(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

def main():
    global uuid, command
    uuid = get_uuid() #inutile car uuid est global
    command = select_os(args) #inutile car uuid est global
    while True:
        send_cached_payloads()
        client()
        sleep(int(args.interval))


if __name__ == "__main__":
    args = parser.parse_args()
    select_logging_mode(args)
    dir_path = os.path.dirname(os.path.realpath(__file__)) ## Get the directory path of the file
    error_logs_file = open(dir_path+'/../logs/error_logs.txt','a')
    debug_logs_file = open(dir_path+'/../logs/debug_logs.txt','a')
    context = daemon.DaemonContext(
        working_directory = dir_path,
        stderr = error_logs_file,
        stdout = debug_logs_file,
        pidfile=pidfile.TimeoutPIDLockFile(PID_FILE)
    )
    with context:
        main()
