import sensorBME280
import sensorCO2
import sensorPM
import converterTime
import time

# Funcion para obtener datos de medicion y enviarlos a firebase y CSV.
def getData(dirFile, module, sessionNumber):
    data = {'timestamp': converterTime.getTimestamp()}
    data.update(sensorBME280.getTHPJSON())

    print data

while True:
    # pedir datos de sensores y guardarlos en un json.
    getData()
    time.sleep(10)

    # enviar los datos a firebase

