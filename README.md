## Installation

### Raspbian system dependencies:

```
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/os-release
echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

sudo apt-get update
sudo apt-get upgrade
sudo apt update && sudo apt install -y influxdb

# for "modern" raspis (2, 3, 4) (armv7):
sudo apt-get install grafana
# for older raspis (Zero, 1) (armv6):
https://raw.githubusercontent.com/trashware/grafana-rpi-zero/master/grafana_6.0.1_armhf.deb
sudo dpkg -i grafana_6.0.1_armhf.deb

sudo systemctl unmask influxdb.service
sudo systemctl start influxdb
sudo systemctl enable influxdb.service

sudo systemctl unmask grafana-server.service
sudo systemctl start grafana-server
sudo systemctl enable grafana-server.service

sudo apt install virtualenv vim python3-smbus fake-hwclock
```

### Influxdb user:
start `influxdb` CLI on the pi and type:

```
create database airquality
use airquality

create user grafana with password 'grafana' with all privileges
grant all privileges on airquality to grafana
```

### Grafana setup:
Point your webbrowser to the IP of the pi on port 3000 (e.g. `http://192.168.100.188:3000`).
Login with the username `admin` and password `admin`, you are free to change that to whatever fits.
Then, add a InfluxDB datasource using `localhost:8089` and the user credentials used above in the influxdb setup.

Import the dashboard from the `grafana.json` file in the repository.

### Setup logging daemon

Checkout the code, install the required python packages and enable/start as a daemon:
```
git clone https://github.com/NerdyProjects/pi_airquality.git airquality
cd airquality
virtualenv venv
. ./venv/bin/activate
pip install -r requirements.txt
sudo cp airquality.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable airquality.service
```

If you use any custom paths/settings, please edit `config.ini` and/or the `airquality.service` systemd file accordingly.

### Auto Wifi
If you want to use the sensor not only at your home with wifi coverage but also abroad, you might want to setup automatic switching between WiFi access point and WiFi client mode.
It should be straightforward to do that in a way similar as described in https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/157-raspberry-pi-auto-wifi-hotspot-switch-internet


