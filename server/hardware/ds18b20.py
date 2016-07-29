import json
import time
 
device_file = '/sys/bus/w1/devices/%s/w1_slave'

def get_devices():
  with open('sensors.json') as f:
    return json.load(f)

def read_temp(device):
  try:
    with open(device_file % device, 'r') as f:
      lines = f.readlines()

    if not lines[0].endswith('YES\n'):
      return '*'

    (_, raw_temp) = lines[1].split('=')
    temp = float(raw_temp) / 1000
    if temp == 85.0:
      return '*'

    return str(temp)
  except IOError:
    return '*'
