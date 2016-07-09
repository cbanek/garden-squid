#!/usr/bin/python
import datetime
import time

import k30
import sht31
import ds18b20

with open("weather.csv", "a") as csv:
  temp_sensors = ds18b20.get_devices()

  header = '# time, co2, humidity, int_temp'

  sensor_ids = []
  for sensor_id, sensor_name in temp_sensors.iteritems():
    header += ', %s' % sensor_name
    sensor_ids.append(sensor_id)

  print header
  csv.write(header + "\n")
  sht = sht31.SHT31()
  co2_sensor = k30.K30()

  while True:
    current_time = datetime.datetime.now()
    (int_temp, humidity) = sht.get_temp_and_humidity()

    co2 = co2_sensor.get_ppm()
    data_line = "%s, %d, %f, %f" % (current_time, co2, humidity, int_temp)

    for sensor_id in sensor_ids:
      data_line += ", " + ds18b20.read_temp(sensor_id)
      time.sleep(.1)

    print data_line
    csv.write(data_line+"\n")
    time.sleep(4)
