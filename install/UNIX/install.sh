# Install sensors
#sudo apt-get install lm-sensors
#sudo sensors-detect --auto

# Put files in /opt/batteryprobe
sudo mkdir -p /opt/batteryprobe/logs /opt/batteryprobe/client
sudo cp -r scrap /opt/batteryprobe
sudo chmod 327 /opt/batteryprobe

# Install python env
cd /opt/batteryprobe
pip install virtualenv
virtualenv probe_env
cd -
source /opt/batteryprobe/probe_env/bin/activate && pip3 install -r client/requirements.txt

# Add batteryprobe service to init.d
sudo cp install/UNIX/batteryprobe /etc/init.d/batteryprobe
sudo chmod +x /etc/init.d/batteryprobe

# Add client to opt dir
sudo cp client/client.py /opt/batteryprobe/client/client.py
sudo chmod +x /opt/batteryprobe/client/client.py
