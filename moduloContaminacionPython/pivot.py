import serial

ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 9600

while(True):
    if(ser.is_open):
        x = ser.read()
        print(x)
    else:
        print("Comunicación Serial cerrada.")