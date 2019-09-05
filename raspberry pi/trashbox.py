import RPi.GPIO as GPIO
import time
import signal
import atexit

atexit.register(GPIO.cleanup)

Frequency = 50  #脉冲频率
init_dutycycle = 7.5
min_dutycycle = 2.5     #角度为0占空比
max_dutycycle = 12.5        #角度为180度占空比

def rotation(servopins):
    print(servopins)
    GPIO.setmode(GPIO.BCM)
    pwms=[]
    for i,servopin in enumerate(servopins):
        GPIO.setup(servopin, GPIO.OUT)
        pwms.append(GPIO.PWM(servopin, Frequency))
        pwms[i].start(init_dutycycle)       #舵机回到初始位置
        print(pwms[i])
    print("open")
    for pwm in pwms:
        pwm.ChangeDutyCycle(2.5)
    print("close")
    time.sleep(3)
    for pwm in pwms:
        pwm.ChangeDutyCycle(7.5)
    time.sleep(0.8)
    time.sleep(2)
    pwm.stop()
    time.sleep(1)
    GPIO.cleanup()



def open(trashtype):
    print("open trashbox")
    #typetonum={"battery":0,"plastic bottle":21,"paper":2,"baozhuangdai":3}
    typetonum={"harmtrash":[12],"cycletrash":[21],"wettrash":[16],"drytrash":[20],"drywettrash":[16,20]}
    rotation(typetonum[trashtype])
    print("done")
'''if __name__ == '__main__':
    servopin = 21
    rotation(21)'''
if __name__ == '__main__':
    open("cycletrash")