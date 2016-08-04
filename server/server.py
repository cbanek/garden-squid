import collections
import csv
import datetime
import json
import time

import flask

app = flask.Flask(__name__)

@app.route("/api/data")
def get_data():
  from_time = flask.request.args.get('from')
  to_time = flask.request.args.get('to')

  from_time = time.mktime(time.strptime(from_time, "%Y-%m-%dT%H:%M:%S"))
  to_time = time.mktime(time.strptime(to_time, "%Y-%m-%dT%H:%M:%S"))

  with open('weather.csv') as data_file:
    reader = csv.DictReader(data_file)
    data = collections.defaultdict(list)

    for row in reader:
      time_string = row['time'].split('.')[0]
      row_time = time.mktime(time.strptime(time_string, "%Y-%m-%d %H:%M:%S"))

      if row_time > from_time and row_time < to_time:
        for field in reader.fieldnames:
          if field != 'time' and row[field] != ' *':
            data[field].append([row_time*1000, float(row[field])])

  return json.dumps(data)

@app.route("/api/sensors", methods=['GET'])
def get_sensors():
  with open('sensors.json') as sensors:
    return sensors.read()

@app.route("/api/sensors", methods=['PUT'])
def put_sensors():
  data = flask.request.get_json()

  with open('sensors.json', 'w') as sensors:
    sensors.write(json.dumps(data))

  return json.dumps(data)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
