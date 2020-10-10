"""Init OSX Agent

Create the XML file batteryprobe.collect.example.plist
and copy it to ~/Library/LaunchAgent/
Allow the daemon to launch at login without interaction needed.
"""

import os
from os.path import join

OSX_DIR = 'OSX_config'
AGENT_FILE_EXAMPLE = 'batteryprobe.collect.example.plist'
AGENT_FILE_TO_CREATE = 'batteryprobe.collect.launchAtLogin.plist'
DIRECTORY = "test/"
VAR_WORKING_DIRECTORY = '$WORKING_DIRECTORY'

"""
Main function
"""
def main():
    dir_path = os.getcwd()
    LOCATION_EXAMPLE_FILE = join(OSX_DIR,AGENT_FILE_EXAMPLE)
    LOCATION_AGENT_FILE = join(OSX_DIR, AGENT_FILE_TO_CREATE)

    os.system('cp '+LOCATION_EXAMPLE_FILE+' '+LOCATION_AGENT_FILE)
    with open(LOCATION_AGENT_FILE, 'r') as file:
        content = file.read()
        updated_file = content.replace(VAR_WORKING_DIRECTORY, dir_path)
        file.close()

    with open(LOCATION_AGENT_FILE, 'w') as file:
        file.write(updated_file)

if __name__ == "__main__":
    main()