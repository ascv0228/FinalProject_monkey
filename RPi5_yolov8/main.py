from Serial import *
import time
import subprocess
import socket
import serial
from multiprocessing import Process, Queue, Value

devices = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2"]

ser = attempt_connection(devices)

host = '192.168.137.62'
port = 12345

def connect_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def process_command(command_queue, subprocess_flag):
    subprocess_instance = None
    while True:
        command = command_queue.get()
        if command == "SystemOn":
            if not subprocess_flag.value:
                subprocess_instance = subprocess.Popen(["/home/anon/miniconda3/envs/yolov8_picam/bin/python", "/home/anon/test/FinalProject_monkey/RPi5_yolov8/nogui.py"])
                subprocess_flag.value = 1
        elif command == "SystemOff" and subprocess_flag.value:
            if subprocess_instance is not None:
                subprocess_instance.terminate()
                subprocess_instance = None
                subprocess_flag.value = 0
        else:
            client_socket = connect_socket(host, port)
            client_socket.sendall(command.encode())
            client_socket.close()

def read_serial(ser, command_queue):
    while True:
        command = read_serial_response(ser)
        print(command)
        command_queue.put(command)
        time.sleep(0.1)

if __name__ == "__main__":
    command_queue = Queue()
    subprocess_flag = Value('i', 0)  # Flag to check if subprocess is running

    process_process = Process(target=process_command, args=(command_queue, subprocess_flag))
    serial_process = Process(target=read_serial, args=(ser, command_queue))

    process_process.start()
    serial_process.start()

    process_process.join()
    serial_process.join()