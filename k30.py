#!/usr/bin/python
import serial
import time


class K30:
  def __init__(self):
    self.ser = serial.Serial("/dev/ttyS0", baudrate=9600)

  def get_ppm(self):
    self.ser.write("\xFE\x44\x00\x08\x02\x9F\x25")
    time.sleep(.01)
    resp = self.ser.read(7)
    co2 = ord(resp[3])*256 + ord(resp[4])
    return co2

if __name__ == "__main__":
    k30 = K30()
    while True:
      print "CO2: %d" % k30.get_ppm()
      time.sleep(1)
