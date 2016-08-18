import collections
import csv
import datetime
import glob
import json
import time
import threading

import flask

import hardware.test
import hardware.k30
import hardware.sht31
import hardware.ds18b20

app = flask.Flask(__name__)

@app.route("/api/data")
def get_data():
  from_time = flask.request.args.get('from')
  to_time = flask.request.args.get('to')

  print 'Graphing from %s to %s' % (from_time, to_time)

  from_time = time.mktime(time.strptime(from_time, "%Y-%m-%dT%H:%M:%S"))
  to_time = time.mktime(time.strptime(to_time, "%Y-%m-%dT%H:%M:%S"))

  data = collections.defaultdict(list)
  data['DEVICE_TIME'] = datetime.datetime.utcnow().isoformat()

  data_files = glob.glob('*.csv')
  data_files.sort()

  last_idx = len(data_files)

  for idx, data_file in enumerate(data_files):
    from_time_filename = time.strftime("%Y-%m-%dT%H:%M:%S.csv", time.localtime(from_time))
    to_time_filename = time.strftime("%Y-%m-%dT%H:%M:%S.csv", time.localtime(to_time))

    next_idx = idx + 1
    if next_idx < last_idx and \
       from_time_filename > data_files[idx] and \
       from_time_filename > data_files[next_idx]:
      print 'Skipping %s (file before time)' % data_file
      continue

    if to_time_filename < data_files[idx]:
      print 'Skipping %s (file after time)' % data_file
      continue

    print 'Searching data file: %s' % data_file

    with open(data_file) as data_file:
      reader = csv.DictReader(data_file)

      for row in reader:
        time_string = row['time'].split('.')[0]
        row_time = time.mktime(time.strptime(time_string, "%Y-%m-%dT%H:%M:%S"))

        if row_time > from_time and row_time < to_time:
          for field in reader.fieldnames:
            if field != 'time' and row[field] != '*':
              data[field].append([row_time*1000, float(row[field])])

  return json.dumps(data)

@app.route("/api/sensors", methods=['GET'])
def get_sensors():
  return json.dumps(getSensorNames())

@app.route("/api/sensors", methods=['PUT'])
def put_sensors():
  data = flask.request.get_json()
  setSensorNames(data)
  return json.dumps(data)

def getSensorNames():
  try:
    with open('names.json', 'r') as name_file:
      return json.loads(name_file.read())
  except IOError:
    print 'names.json does not exist.'
    return {}

def setSensorNames(names):
  global restartEvent

  with open('names.json', 'w') as name_file:
    name_file.write(json.dumps(names))

  restartEvent.set()

def initSensors():
  global restartEvent
  restartEvent = threading.Event()

  sensors = []
  sensors.extend(hardware.sht31.detect())
  sensors.extend(hardware.k30.detect())
  sensors.extend(hardware.ds18b20.detect())

  if not sensors:
    sensors.extend(hardware.test.detect())

  names = getSensorNames()

  for sensor in sensors:
    sensor_id = sensor['id']
    if sensor_id not in names:
      names[sensor_id] = ''

  setSensorNames(names)
  restartEvent.clear()
  return sensors

def pollThread():
  print 'Starting poll thread.'
  sensors = initSensors()

  while True:
    try:
      names = getSensorNames()

      for sensor in sensors:
        sensor_id = sensor['id']
        if names[sensor_id] != '':
          sensor['name'] = names[sensor_id]

      pollSensors(sensors)
    except Exception as e:
      print 'Exception reading sensors %s' % e

def pollSensors(sensors):
  global restartEvent
  fields = ['time']

  for sensor in sensors:
    if 'name' in sensor:
      fields.append(sensor['name'])

  filename = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.csv")
  print 'Starting new file: %s' % filename

  with open(filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()

    while not restartEvent.wait(5):
      samples = {'time': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}

      for sensor in sensors:
        if 'name' in sensor:
          samples[sensor['name']] = sensor['driver']()

      writer.writerow(samples)
      csvfile.flush()

  restartEvent.clear()

if __name__ == "__main__":
  pollingThread = threading.Thread(target=pollThread)
  pollingThread.daemon = True
  pollingThread.start()
  app.run(debug=True, host='0.0.0.0', use_reloader=False)
