import serial

ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 9600

encoding = 'utf-8'

while(True):
    if(ser.is_open):
        x = ser.read_until()
        x = x.decode(encoding)
        if(len(x) < 20):
            print(x)
    else:
        print("Comunicación Serial cerrada.")
