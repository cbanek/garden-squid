import glob

devices_dir = '/sys/bus/w1/devices/'
devices_glob = devices_dir + '28-*'
device_file = '/sys/bus/w1/devices/%s/w1_slave'

def detect():
  devices = []
  files = glob.glob(devices_glob)

  for file in files:
    serial_num = file[len(devices_dir):]
    temp_id = 'ds18b20-' + serial_num
    devices.append({'id': temp_id, 'driver': DS18B20(serial_num).sample})
    print 'DS18B20: %s' % serial_num

  return devices

class DS18B20:
  def __init__(self, device):
    self.device = device

  def sample(self):
    try:
      with open(device_file % self.device, 'r') as f:
        lines = f.readlines()

      if not lines[0].endswith('YES\n'):
        return '*'

      (_, raw_temp) = lines[1].split('=')
      temp = float(raw_temp) / 1000
      if temp == 85.0:
        return '*'

      return str(temp)
    except IOError as e:
      print e
      return '*'
