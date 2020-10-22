set -e

INIT_D_DIR=/etc/init.d
INSTALL_DIR=/opt/batteryprobe

# Install sensors
echo "Install sensors"
sudo apt-get install lm-sensors
sudo sensors-detect --auto

# Put files in /opt/batteryprobe
echo "Move client and scraping script to " $INSTALL_DIR 
sudo mkdir -p $INSTALL_DIR/logs $INSTALL_DIR/client
sudo cp -r scrap $INSTALL_DIR
sudo chmod 327 $INSTALL_DIR

# Install python env
echo "Install python env"
cd $INSTALL_DIR
pip3 install virtualenv
virtualenv probe_env
cd -
source $INSTALL_DIR/probe_env/bin/activate && pip3 install -r client/requirements.txt

# Add batteryprobe service to init.d
echo "Add service to " $INIT_D_DIR
sudo cp install/UNIX/batteryprobe $INIT_D_DIR/batteryprobe
sudo chmod +x $INIT_D_DIR/batteryprobe

# Add client to install dir
echo "Add client to " $INSTALL_DIR
sudo cp client/client.py  $INSTALL_DIR/client/client.py
sudo chmod +x $INSTALL_DIR/client/client.py

# Reload daemons
systemctl daemon-reload
sudo update-rc.d batteryprobe defaults
