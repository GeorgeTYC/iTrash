from smbus import SMBus
from PCA9685 import PWM  # 从PCA9685引入PWM
import time

fPWM = 50
i2c_address = 0x40  # (standard) 根据连接舵机的接口设置I2C地址
servoNum = 0  # 舵机连接的控制板接口

a = 8.5  # 与舵机相匹配,180度时PWM占空比
b = 2  # 与舵机相匹配,0度时PWM占空比


def setup():
    global pwm
    bus = SMBus(1)  # Raspberry Pi revision 2
    pwm = PWM(bus, i2c_address)
    pwm.setFreq(fPWM)


def setDirection(channel, direction):
    duty = a / 180 * direction + b
    pwm.setDuty(channel, duty)
    print("direction =", direction, "-> duty =", duty)


def rotage(servoNum):
    setDirection(servoNum, 180)
    time.sleep(10)
    setDirection(servoNum, 0)

print("starting")
setup()
rotage(0)
direction = 0
for channel in range(4):
    setDirection(channel, 0)
print("done")
