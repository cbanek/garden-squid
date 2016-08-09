import datetime

def detect():
  return [
    {
      'id': 'test-id1',
      'driver': TestSensor().sample,
      'name': 'test1'
    },
    {
      'id': 'test-id2',
      'driver': TestSensor().sample
    }
  ]

class TestSensor:
  def sample(id):
    return datetime.datetime.now().microsecond
