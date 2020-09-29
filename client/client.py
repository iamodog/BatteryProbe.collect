""""""


import sys
import logging
import argparse
import subprocess
from time import sleep 

import requests


logging.basicConfig(level=logging.INFO)
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


def client():
    if args.mac_os:
        command = "scrap/macOS/scrap.sh"
    elif args.linux:
        command = "scrap/Linux/scrap.sh"
    else:
        raise AssertionError("OS not specified") 
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
    logging.info(payload)  # TODO: remove this

    # Send payload
    response = requests.post(
        f"http://{args.database_uri}/write?db=monitoring&precision=s",
        headers={"Content-type": "text/xml"}, 
        data=payload,
    )
    if 400 <= response.status_code < 500:
        logging.error(f"InfluxDB could not understand the request. \
            Reponse: {response.json()}"
        )
        sys.exit(1)
    elif 500 <= response.status_code:
        logging.error(f"The system is overloaded or significantly impaired. \
            Reponse: {response.json()}"
        )
        sys.exit(1)


def format_payload(data):
    # [measurement],[tag=,tag=] value=[value] [epoch]
    
    data = {
        el.split(",")[0]: el.split(",")[1] 
        for el in data.split("\n") 
        if len(el) != 0 and el.split(",")[1] != "" 
    }
    epoch = data["epoch"]
    del data["epoch"]
    tags = {key[1:]: value for key, value in data.items() if key.startswith("@")}
    if len(tags) == 0:
        logging.error("No tags found")
        sys.exit(1)
    for key in tags:
        del data["@"+key]
 
    payload = ""
    for measurement, value_m in data.items():
        payload += f"{measurement}"
        for tag, value_t in tags.items():
            payload += f",{tag}={value_t}"
        payload += f" value={value_m} {epoch}\n"  
    return payload


def main():
    while True:
        client()
        sleep(int(args.interval))


if __name__ == "__main__":
    args = parser.parse_args()
    main()
