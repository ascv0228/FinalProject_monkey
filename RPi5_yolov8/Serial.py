import serial

def attempt_connection(devices):
    for device in devices:
        try:
            ser = serial.Serial(device,115200,timeout=1)
            print(f"Connected to {device}")
            return ser
        except serial.SerialException:
                print(f"Failed to connect to {device}")
    return None
    
def send_serial_command(ser,command):
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    ser.write(command.encode())
    
    
def read_serial_response(ser):
    while True:
        if ser.in_waiting>0:
            line=ser.readline().decode('utf-8').rstrip()
            return line

    
