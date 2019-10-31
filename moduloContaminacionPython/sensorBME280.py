# REF: https://pypi.org/project/RPi.bme280/

import smbus2
import bme280


def getTHPJSON():
  port = 1
  address = 0x76
  bus = smbus2.SMBus(port)

  calibration_params = bme280.load_calibration_params(bus, address)

  # the sample method will take a single reading and return a
  # compensated_reading object
  data = bme280.sample(bus, address, calibration_params)

  # C, hPa, %
  return {'t': data.temperature, 'h': data.humidity, 'p': data.pressure}
