#!/usr/bin/env python3

from config import *  # pylint: disable=unused-wildcard-import
import w1thermsensor
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
import json
import time
import pika
from dotenv import load_dotenv
import datetime
import os

TERMNINAL_ID = os.environ.get("TERMINAL_ID")
CP_IP = os.environ.get("CP_IP")
CP_PORT = os.environ.get("CP_PORT")

CHANNEL_NAME = os.environ.get("CHANNEL_NAME")

PLAIN_USER = os.environ.get("PLAIN_USER")
PLAIN_PASS = os.environ.get("PLAIN_PASS")

load_dotenv()
credentials = pika.PlainCredentials(PLAIN_USER, PLAIN_PASS)
parameters = pika.ConnectionParameters(
    CP_IP,
    CP_PORT,
    CHANNEL_NAME,
    credentials
)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.queue_declare(CHANNEL_NAME)


def bme280():
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    bme280.sea_level_pressure = 1013.25
    #bme280.mode = adafruit_bme280.MODE_NORMALpi
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
    bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    dic = {}
    dic["sensor"] = int(TERMNINAL_ID) if TERMNINAL_ID else 0
    dic["temperature"] = bme280.temperature
    dic["humidity"] = bme280.humidity
    dic["pressure"] = bme280.pressure
    dic["altitude"] = bme280.altitude
    dic["timestamp"] = str(datetime.datetime.now())

    print(json.dumps(dic))
    channel.basic_publish(exchange="", routing_key="pogoda", body=json.dumps(dic))

def main():
    while True:
        bme280()
        time.sleep(4)
    else:
        GPIO.cleanup()  # pylint: disable=no-member



if __name__ == "__main__":
    main()
