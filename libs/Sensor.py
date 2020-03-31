import RPi.GPIO as GPIO


def isRegPin(func):
    """ 装饰器：校验引脚是否注册 """

    def wrap(this, pin, data):
        pin = list(filter(lambda p: p['number'] == pin, this.pins))
        if len(pin) > 0:
            pin = pin[0]
            return func(this, pin, data)
        else:
            print('该对象没有注册此引脚')

    return wrap


def isIn(func):
    """ 装饰器：校验引脚是否是输入模式 """

    def wrap(this, pin, data):
        if pin['mode'] != 'in':
            print('该引脚不是输入模式')
        else:
            func(this, pin['number'], data)

    return wrap


def isOut(func):
    """ 装饰器：校验引脚是否是输出模式 """

    def wrap(this, pin, data):
        if pin['mode'] != 'out':
            print('该引脚不是输出模式')
        else:
            func(this, pin['number'], data)

    return wrap


class Sensor(object):
    """ 传感器类 """

    def __init__(self, **kwargs):
        self.pins = kwargs['pins']
        # 设置GPIO模式为BOARD
        GPIO.setmode(GPIO.BOARD)
        # 设置引脚模式
        for pin in self.pins:
            if pin['mode'] == 'in':
                GPIO.setup(pin['number'], GPIO.IN)
            elif pin['mode'] == 'out':
                GPIO.setup(pin['number'], GPIO.OUT)

    @isRegPin
    @isIn
    def read_data(self, pin):
        """
            读取引脚数据
            :param pin: 引脚
            :return True | False
        """

        return GPIO.input(pin)

    @isRegPin
    @isOut
    def write_data(self, pin, data):
        """
            向引脚写入数据
            :param pin: 引脚
            :param data: True(高电平) | False(低电平)
            :return: None
        """

        GPIO.output(pin, GPIO.HIGH) if data else GPIO.output(pin, GPIO.LOW)
