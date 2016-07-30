import collections
import csv
import datetime
import json
import time

import flask

app = flask.Flask(__name__)

@app.route("/api/data")
def get_data():
  current_time = datetime.datetime.now()
  default_window = current_time - datetime.timedelta(hours=24)
  from_time = flask.request.args.get('from', default_window)
  to_time = flask.request.args.get('to', current_time)

  with open('weather.csv') as data_file:
    reader = csv.DictReader(data_file)
    data = collections.defaultdict(list)

    for row in reader:
      time_string = row['time'].split('.')[0]
      row_time = time.mktime(time.strptime(time_string, "%Y-%m-%d %H:%M:%S"))
      row_datetime = datetime.datetime.fromtimestamp(row_time)

      if row_datetime > from_time and row_datetime < to_time:
        for field in reader.fieldnames:
          if field != 'time' and row[field] != ' *':
            data[field].append([row_time*1000, float(row[field])])

  return json.dumps(data)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
