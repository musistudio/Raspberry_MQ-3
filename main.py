import time
import RPi.GPIO as GPIO
from libs.Sensor import Sensor
from libs.mq import *
from libs.LCD import LCD1602
import json
import os

# 禁用GPIO警告
GPIO.setwarnings(False)


def get_config():
    with open(f'./config.json', 'r') as f:
        config = json.loads(f.read())
    return config


class LED(Sensor):
    def write_data(self, pin, data):
        if data:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.3)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.3)
        else:
            GPIO.output(pin, GPIO.LOW)


if __name__ == "__main__":
    config = get_config()
    sleep_seconds = 1  # 间隔秒数
    threshold = 1      # 报警阈值
    lcd = LCD1602(config['LCD']['RS'], config['LCD']['E'], config['LCD']['D4'], config['LCD']['D5'],
                  config['LCD']['D6'], config['LCD']['D7'])
    lcd.lcd_string('initing...', 1)
    mq = MQ()
    # 注册LED对象
    led = LED(pins=[
        {"number": config['LED']['pin'], "mode": "out"}
    ])
    # 注册蜂鸣器对象
    buzzer = Sensor(pins=[
        {"number": config['buzzer']['pin'], "mode": "out"}
    ])
    while True:
        try:
            perc = mq.MQPercentage()
            # 将ppm单位转成mg/m3
            # 根据链接：https://blog.csdn.net/zhuisaozhang1292/article/details/84983874
            alcohol = (perc["GAS_LPG"] * 46) / 24.45
            if alcohol > threshold:
                led.write_data(config['LED']['pin'], True)
                buzzer.write_data(config['buzzer']['pin'], True)
            else:
                led.write_data(config['LED']['pin'], False)
                buzzer.write_data(config['buzzer']['pin'], False)
            lcd.lcd_string("alcohol:", 1)
            lcd.lcd_string("%.2f mg/m³" % alcohol, 2)
            time.sleep(sleep_seconds)
        except ValueError:
            lcd.lcd_string("alcohol: ERROR", 1)
            time.sleep(sleep_seconds)
        except KeyboardInterrupt:
            lcd.cleanup()
            GPIO.cleanup()
            print('退出程序')
