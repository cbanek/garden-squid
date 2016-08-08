import datetime

def detect():
  return [
    {
      'id': 'test-id1',
      'driver': TestSensor(),
      'name': 'test1'
    },
    {
      'id': 'test-id2',
      'driver': TestSensor()
    }
  ]

class TestSensor:
  def sample(id):
    return datetime.datetime.now().microsecond
