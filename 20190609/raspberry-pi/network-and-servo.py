import socket
import RPi.GPIO as GPIO
import time

pan_pin = 12
tilt_pin = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(pan_pin, GPIO.OUT)
GPIO.setup(tilt_pin, GPIO.OUT)

pan_pwm = GPIO.PWM(pan_pin, 50)
tilt_pwm = GPIO.PWM(tilt_pin, 50)

pan_pwm.start(0)
tilt_pwm.start(0)

pan_pwm.ChangeDutyCycle(7)
tilt_pwm.ChangeDutyCycle(6)

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind(('0.0.0.0', 1025))

while True:
    data, addr = soc.recvfrom(1024)

    data = data.decode()
    
    slice_index = data.index('/')
    
    pan_pos = float(data[0:slice_index])
    tilt_pos = float(data[slice_index+1:])
    
    print(pan_pos, tilt_pos)
    
    pan_pwm.ChangeDutyCycle(pan_pos)
    tilt_pwm.ChangeDutyCycle(tilt_pos)
