import serial
import log
import timeCustom
import goToFirebase

ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 9600

encoding = 'utf-8'

while(True):
    if(ser.is_open):
        data = {}
        x = ser.read_until()
        x = x.decode(encoding)
        contenido = x.split(':')
        if(contenido[0] == 'ERROR'):
            log.recivedErrorArduino(timeCustom.getCurrenDateAndTimeSTR() , contenido[1])
        elif(contenido[0] == 'WARNING'):
            print(x)
        elif(len(contenido) < 2):
            print("hubo error desconocido")
            print(contenido)
        else:
            data.update({contenido[0]: contenido[1].replace('\r\n',''), 'timestamp': timeCustom.getTimestamp()})
            goToFirebase.send(timeCustom.getTimestamp(), contenido[0], contenido[1])
            print(data)
            log.saveBackup(data)
    else:
        print('Serial esta cerrado')
