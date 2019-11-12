import csv
import os.path as path

fieldNames = ['param', 'value', 'dataTime']

def createFile(nameFile):
    # Crear nombre del archivo
    with open(nameFile, 'a') as csvfile:
        write = csv.DictWriter(csvfile, fieldnames = fieldNames)
        write.writeheader()
    print("Generando nuevo archivo")

def writeData(param, value, dataTime, nameFile):
    if (path.exists(nameFile) != True ):
        createFile(nameFile)
    data = {'param': param, 'value': value, 'dataTime': dataTime}
    with open(nameFile, 'a') as csvfile:
        write = csv.DictWriter(csvfile, fieldnames = fieldNames)
        write.writerow(data)
        print("Escrito con exito en CSV.")