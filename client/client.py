""""""


import subprocess


if __name__ == "__main__":
    command = "./scrap.sh"
    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE
    )
    if result.returncode == 0:
        data = result.stdout.decode("utf-8")
        # split rows
        columns = data.split("\n")
        print(columns)
        for col in columns[:-1]:
            print(col.split(","))
