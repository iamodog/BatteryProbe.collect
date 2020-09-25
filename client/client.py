""""""
import subprocess
from time import sleep 

def client():
    command = "scrap/MACOS/scrap.sh"
    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE
    )
    with open("/tmp/passage.txt", "a") as f:
        f.write("Un passage ici\n")
    if result.returncode == 0:
        data = result.stdout.decode("utf-8")
        # split rows
        columns = data.split("\n")
        print(columns)
        for col in columns[:-1]:
            print(col.split(","))

def main():
    while True:
        client()
        sleep(10)


if __name__ == "__main__":
    main()
