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
FINAL_LOCATION_AGENT_FILE = '~/Library/LaunchAgents'
EXECUTABLE_FILE = 'client/client.py'
STD_ERR_FILE = 'stderr.log'
STD_OUT_FILE = 'stdout.log'
DATABASE = '54.38.188.95:8086'
PYTHON_ENV = 'probe_env/bin/activate'


# Vars to replace in the example.plist
CONST_WORKING_DIRECTORY = '$WORKING_DIRECTORY'
CONST_OSX_DIR = '$OSX_DIR'
CONST_STD_ERR_LOG = '$STD_ERR_LOG'
CONST_STD_OUT_LOG = '$STD_OUT_LOG'
CONST_DATABASE = '$DATABASE'
CONST_EXECUTABLE = '$EXECUTABLE'
CONST_PYTHON_ENV = '$PYTHON_ENV'

"""
Main function
"""
def agent_install():
    #Init some variables
    dir_path = os.getcwd()
    LOCATION_EXAMPLE_FILE = join(OSX_DIR,AGENT_FILE_EXAMPLE)
    LOCATION_AGENT_FILE = join(OSX_DIR, AGENT_FILE_TO_CREATE)

    #Copy the example.plist to launchAtLogin.plist
    os.system('cp '+LOCATION_EXAMPLE_FILE+' '+LOCATION_AGENT_FILE)

    #Replace content of launchAtLogin.plist according to the actual configuration
    with open(LOCATION_AGENT_FILE, 'r') as file:
        content = file.read()
        updated_file = content\
            .replace(CONST_WORKING_DIRECTORY, dir_path)\
            .replace(CONST_OSX_DIR, OSX_DIR)\
            .replace(CONST_STD_ERR_LOG, STD_ERR_FILE)\
            .replace(CONST_STD_OUT_LOG, STD_OUT_FILE)\
            .replace(CONST_DATABASE, DATABASE)\
            .replace(CONST_EXECUTABLE, EXECUTABLE_FILE)\
            .replace(CONST_PYTHON_ENV,PYTHON_ENV)
        file.close()

    #Save the updated_file
    with open(LOCATION_AGENT_FILE, 'w') as file:
        file.write(updated_file)

    #Copy the updated file to final location in MacOs
    os.system('cp '+ LOCATION_AGENT_FILE+' '+FINAL_LOCATION_AGENT_FILE)

    os.system('launchctl load '+FINAL_LOCATION_AGENT_FILE+'/'+AGENT_FILE_TO_CREATE)

def env_install():
    # Need istats
    os.system('pip3 install virtualenv')
    os.system('virtualenv probe_env')
    os.system('source '+PYTHON_ENV)
    os.system('pip3 install -r ./'+OSX_DIR+'/requirements.txt')
    os.system('ls')

if __name__ == "__main__":
    env_install()
    agent_install()