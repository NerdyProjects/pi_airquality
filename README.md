## Installation

Raspbian system dependencies:
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

create influxdb user:
```
create database airquality
use home

create user grafana with password 'grafana' with all privileges
grant all privileges on airquality to grafana

```

Setup influx db dataasource in grafana (IP:3000, admin // admin)

```
git clone airquality
sudo cp airquality.service /etc/systemd/system
