import RPi.GPIO as GPIO
import time


LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

E_PULSE = 0.0001
E_DELAY = 0.0001


class LCD1602(object):

    def __init__(self, rs, e, d4, d5, d6, d7):
        self.LCD_RS = rs
        self.LCD_E = e
        self.LCD_D4 = d4
        self.LCD_D5 = d5
        self.LCD_D6 = d6
        self.LCD_D7 = d7
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.LCD_E, GPIO.OUT)
        GPIO.setup(self.LCD_RS, GPIO.OUT)
        GPIO.setup(self.LCD_D4, GPIO.OUT)
        GPIO.setup(self.LCD_D5, GPIO.OUT)
        GPIO.setup(self.LCD_D6, GPIO.OUT)
        GPIO.setup(self.LCD_D7, GPIO.OUT)
        self.lcd_init()


    def lcd_init(self):
        self.lcd_byte(0x33, LCD_CMD)
        self.lcd_byte(0x32, LCD_CMD)
        self.lcd_byte(0x06, LCD_CMD)
        self.lcd_byte(0x0C, LCD_CMD)
        self.lcd_byte(0x28, LCD_CMD)
        self.lcd_byte(0x01, LCD_CMD)
        time.sleep(E_DELAY)

    def lcd_byte(self, bits, mode):
        GPIO.output(self.LCD_RS, mode)
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits & 0x10 == 0x10:
            GPIO.output(self.LCD_D4, True)
        if bits & 0x20 == 0x20:
            GPIO.output(self.LCD_D5, True)
        if bits & 0x40 == 0x40:
            GPIO.output(self.LCD_D6, True)
        if bits & 0x80 == 0x80:
            GPIO.output(self.LCD_D7, True)
        self.lcd_toggle_enable()
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits & 0x01 == 0x01:
            GPIO.output(self.LCD_D4, True)
        if bits & 0x02 == 0x02:
            GPIO.output(self.LCD_D5, True)
        if bits & 0x04 == 0x04:
            GPIO.output(self.LCD_D6, True)
        if bits & 0x08 == 0x08:
            GPIO.output(self.LCD_D7, True)
        self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
        time.sleep(E_DELAY)
        GPIO.output(self.LCD_E, True)
        time.sleep(E_PULSE)
        GPIO.output(self.LCD_E, False)
        time.sleep(E_DELAY)

    def lcd_string(self, message, line):
        line = 0xC0 if line == 2 else 0x80
        message = message.ljust(LCD_WIDTH, " ")
        self.lcd_byte(line, LCD_CMD)
        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)

    def cleanup(self):
        self.lcd_byte(0x01, LCD_CMD)
        self.lcd_string("quitting...", 1)

