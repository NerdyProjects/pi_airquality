from smbus2 import SMBus, i2c_msg
from bme280 import BME280
from sgp30 import SGP30
from pms5003 import PMS5003
from datetime import datetime
import time
import sys
import math
import threading
import influxdb
import configparser
import os


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
influxdb_client = influxdb.InfluxDBClient(
  config.get('influxdb', 'host'),
  config.getint('influxdb', 'port'),
  config.get('influxdb', 'username'),
  config.get('influxdb', 'password'),
  config.get('influxdb', 'database'),
  config.getboolean('influxdb', 'ssl'),
  verify_ssl=True,
  timeout=5,
  retries=5,
)

i2c_dev = SMBus(1)

sgp30 = SGP30(i2c_dev, i2c_msg)
bme280 = BME280(i2c_dev=i2c_dev)
pms5003 = PMS5003(
    device='/dev/ttyAMA0',
    baudrate=9600,
    pin_enable=22,
    pin_reset=27
)
pmsdata = [None]

def pms_read_loop():
    while True:
        pmsdata[0] = pms5003.read()

print("SGP30 warming up, please wait...")
def crude_progress_bar():
    sys.stdout.write('.')
    sys.stdout.flush()

sgp30.start_measurement(crude_progress_bar)
sys.stdout.write('\n')
print("Start logging.")
temperature = bme280.get_temperature()
pms_read_thread = threading.Thread(target=pms_read_loop)
pms_read_thread.start()
count = 0
while True:
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    absolute_humidity = humidity*6.112*2.1674*math.e**((temperature*17.67)/(temperature+243.5))/(temperature+273.15)
    sgp30.command('set_humidity', [int(absolute_humidity*256)])
    airquality = sgp30.get_air_quality()
    time.sleep(1.0)
    count = count + 1

    if count % 10 == 0:
      influxdb_client.write_points(
              [{"measurement": 'airquality',
                  "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                  "fields": {'temperature': temperature,
                      'pressure': pressure,
                      'relative_humidity': humidity,
                      'absolute_humidity': absolute_humidity,
                      'equivalent_co2': airquality.equivalent_co2,
                      'total_voc': airquality.total_voc,
                      'pm1': pmsdata[0].pm_ug_per_m3(1.0),
                      'pm2.5': pmsdata[0].pm_ug_per_m3(2.5),
                      'pm10': pmsdata[0].pm_ug_per_m3(10.0),
                      'a_pm1': pmsdata[0].pm_ug_per_m3(1.0, True),
                      'a_pm2.5': pmsdata[0].pm_ug_per_m3(2.5, True),
                      'a_pm10': pmsdata[0].pm_ug_per_m3(None, True),
                      'pm0.3_l': pmsdata[0].pm_per_1l_air(0.3),
                      'pm0.5_l': pmsdata[0].pm_per_1l_air(0.5),
                      'pm1.0_l': pmsdata[0].pm_per_1l_air(1.0),
                      'pm2.5_l': pmsdata[0].pm_per_1l_air(2.5),
                      'pm5.0_l': pmsdata[0].pm_per_1l_air(5),
                      'pm10.0_l': pmsdata[0].pm_per_1l_air(10)}}],
        time_precision="ms")


