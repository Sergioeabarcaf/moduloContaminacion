# REF : https://github.com/bfaliszek/Python-HPMA115S0

import serial, time
from time import localtime, strftime

port = serial.Serial("/dev/serial0", baudrate=9600, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout=1.5)

def main():
    if port.isOpen():
        port.close()
    port.open()
    time.sleep(0.1)
    data = port.read(32)
    time.sleep(0.1)
    print data
    try:
        if ord(data[0]) == 66 and ord(data[1]) == 77:
            suma = 0
            for a in range(30):
                suma += ord(data[a])
            if suma == ord(data[30])*256+ord(data[31]):
                PM25 = int(ord(data[6])*256+ord(data[7]))
                PM10 = int((ord(data[8])*256+ord(data[9]))/0.75)
                print 'PM2.5: %d ug/m3' % round(PM25)
                print 'PM10: %d ug/m3' % round(PM10)
                datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())
            else
                print "no data"
        else:
            print "no data"
    except Exception as ex:
        print ex
    finally:
        port.close()

if __name__=="__main__":
    for a in range(35):
        main()
        time.sleep(0.2)