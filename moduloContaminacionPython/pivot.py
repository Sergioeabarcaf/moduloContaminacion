import serial
import time

ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 9600

encoding = 'utf-8'

while(True):
    if(ser.is_open):
        data = {}
        x = ser.read_until()
        x = x.decode(encoding)
        contenido = x.split(':')
        if(contenido[0] != 'WARNING'):
            data.update(contenido[0]:contenido[1], 'timestamp': time.time())
            print(data)

        if(contenido[0] == 'ERROR'):
            print(x)
    else:
        print('Comunicación Serial cerrada.')

