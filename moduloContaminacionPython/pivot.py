import serial
import log
import timeCustom
import goToFirebase
import csvFile

ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 9600

encoding = 'utf-8'

while(True):
    # Validar la comunicacion serial con arduino
    if(ser.is_open):
        x = ser.read_until()
        x = x.decode(encoding)
        contenido = x.split(':')
        # Almacenar el error recibido por parte del arduino
        if(contenido[0] == 'ERROR'):
            log.recivedErrorArduino(timeCustom.getCurrenDateAndTimeSTR() , contenido[1])
        # Mostrar los mensajes de WARNING desde arduino
        elif(contenido[0] == 'WARNING'):
            print(x)
        # En caso de no cumplir con la cantidad de contenido, se muestra un mensaje 
        elif(len(contenido) < 2):
            print("hubo error desconocido")
            print(contenido)
        # Se procesa el mensaje para ser almacenado en csv y enviarlo a Firebase.
        else:
            # Eliminar basura del valor
            contenido[1] = contenido[1].replace('\r\n','')
            # Parche para solucionar problema con PM2.5
            if(contenido[0] == "PM2.5"):
                contenido[0] = "PM2-5"
            # Enviar los datos a Firebase
            goToFirebase.send(timeCustom.getTimestamp(), contenido[0], contenido[1])
            # Almacenar los datos a nivel local en CSV.
            csvFile.writeData(contenido[0], contenido[1], timeCustom.getTimestamp(), timeCustom.getCurrentDateSTR() + '.csv')

    else:
        print('Serial esta cerrado')
