import RPi.GPIO as GPIO
import smbus
import time
import socket
from gpiozero import Buzzer

unlock=12
lock=9

def writeData(value):
    bus.write_byte(address, value)  
    return -1

host = '192.168.137.62'
port = 12345

address = 0x08  
bus = smbus.SMBus(1)  
GPIO.setmode(GPIO.BOARD)

buzzer = Buzzer(22)
GPIO.setup(11, GPIO.OUT) 
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
servo1 = GPIO.PWM(11, 50)  
servo2 = GPIO.PWM(12, 50)
servo3 = GPIO.PWM(13, 50)

servo1.start(0)
servo2.start(0)
servo3.start(0)
time.sleep(0.05)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port))

while(1):
    server_socket.listen(5)

    print("等待客戶端連線...")

    client_socket, addr = server_socket.accept()
    print("客戶端已連線：", addr)

    data = client_socket.recv(1024)
    print("接收到的資料：", data.decode())
    data=data.decode()
    if data == "Unlock1":
        servo1.ChangeDutyCycle(unlock)
        time.sleep(1)   
    elif data == "Unlock2":
        servo2.ChangeDutyCycle(unlock)
        time.sleep(1)
    elif data == "Unlock3":
        servo3.ChangeDutyCycle(unlock)
        time.sleep(1)
    elif data == "UnlockAll":
        servo1.ChangeDutyCycle(unlock)  
        servo2.ChangeDutyCycle(unlock) 
        servo3.ChangeDutyCycle(unlock)
        time.sleep(1)

    elif data == "Lock1":
        servo1.ChangeDutyCycle(lock)
        time.sleep(1)
    elif data == "Lock2":
        servo2.ChangeDutyCycle(lock)
        time.sleep(1)
    elif data == "Lock3":
        servo3.ChangeDutyCycle(lock)
        time.sleep(1)
    elif data == "LockAll":
        servo1.ChangeDutyCycle(lock)
        servo2.ChangeDutyCycle(lock) 
        servo3.ChangeDutyCycle(lock)
        time.sleep(1)

    elif data == "Bon":
        buzzer.on()
        time.sleep(1)
    elif data == "Boff":
        buzzer.off()
        time.sleep(1)

    servo1.ChangeDutyCycle(0)  
    servo2.ChangeDutyCycle(0) 
    servo3.ChangeDutyCycle(0)
    
servo1.stop()
servo2.stop()
servo3.stop()   
GPIO.cleanup()
client_socket.close()
server_socket.close()
