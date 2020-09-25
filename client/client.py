""""""


import argparse
import subprocess
from time import sleep 


parser = argparse.ArgumentParser()
parser.add_argument(
    "--linux",
    action="store_true"
)
parser.add_argument(
    "--mac_os",
    action="store_true"
)
parser.add_argument(
    "--interval",
    default=10,
    help="Data scrapping frequency (in seconds)"
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
        data = result.stdout.decode("utf-8")
        columns = data.split("\n")
        for col in columns[:-1]:
            print(col.split(","))

    # Send payload
    # requests


def main():
    while True:
        client()
        sleep(int(args.interval))


if __name__ == "__main__":
    args = parser.parse_args()
    main()
