// LIBRERIAS ------------------------------------------------------
// BME280 ////////////////////////////////////////////////////////
#include <BME280I2C.h>
#include <Wire.h>

// CO2 ///////////////////////////////////////////////////////////
#include "Adafruit_CCS811.h"

// PM ////////////////////////////////////////////////////////////
#include <Arduino.h>
#include <SoftwareSerial.h>

// DHT11 ////////////////////////////////////////////////////////////
#include <DHT.h>



// VARIABLES -----------------------------------------------------
#define SERIAL_BAUD 9600
#define seconds 60000
String aux;

// BME280 /////////////////////////////////////////////////////////
BME280I2C bme;
String tempBMStr = "BM-T:";
String humBMStr = "BM-H:";
String presBMStr = "BM-P:";
float tempBMValue(NAN), humBMValue(NAN), presBMValue(NAN);

// CO2 ////////////////////////////////////////////////////////////
Adafruit_CCS811 ccs;
String co2Str = "CO2:";
float co2Value;

// PM /////////////////////////////////////////////////////////////
#define LENG 31   //0x42 + 31 bytes equal to 32 bytes
unsigned char buf[LENG];
String pm1Str = "PM1:";
String pm25Str = "PM2-5:";
String pm10Str = "PM10:";
int PM01Value=0;
int PM2_5Value=0;
int PM10Value=0;
SoftwareSerial PMSerial(10, 11); // RX, TX

// Light ambient //////////////////////////////////////////////////
#define lightPin 0
String lightStr = "L:";
int lightValue = 0;

// DHT //////////////////////////////////////////////////
#define pindht 2
#define DHTTYPE DHT22 // DHT 22 (AM2302)
DHT dht (pindht, DHTTYPE);
String tempDHStr = "DH-T:";
String humDHStr = "DH-H:";
float tempDHValue, humDHValue;



// Setup //////////////////////////////////////////////////////////
void setup(){
  setupBME280();
  setupCO2();
  setupPM();
  delay(120000);
}



// loop ///////////////////////////////////////////////////////////
void loop(){
   Serial.begin(SERIAL_BAUD);
   dataBME280();
   dataCO2();
   dataPM();
   dataLight();
   dataDHT();
   Serial.flush();
   Serial.end();
   delay(seconds);
}



// FUNCIONES ------------------------------------------------------
// Funciones BME280 ////////////////////////////////////////////////
void setupBME280(){
  while(!Serial) {} // Wait
  Wire.begin();
  while(!bme.begin()){
    Serial.println("ERROR: Could not find BME280 sensor!");
    delay(1000);
  }
  
  switch(bme.chipModel()){
     case BME280::ChipModel_BME280:
       Serial.println("WARNING:Found BME280 sensor! Success.");
       break;
     case BME280::ChipModel_BMP280:
       Serial.println("WARNING:Found BMP280 sensor! No Humidity available.");
       break;
     default:
       Serial.println("WARNING:Found UNKNOWN sensor! Error!");
  }
}

void dataBME280(){
  BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
  BME280::PresUnit presUnit(BME280::PresUnit_hPa);
  bme.read(presBMValue, tempBMValue, humBMValue, tempUnit, presUnit);

  aux = tempBMStr + tempBMValue;
  Serial.println(aux);
  aux = humBMStr + humBMValue;
  Serial.println(aux);
  aux = presBMStr + presBMValue;
  Serial.println(aux);
}


// Funciones CO2 ////////////////////////////////////////////////////
void setupCO2(){
  if(!ccs.begin()){
    Serial.println("ERROR:Fallo en sensor CO2");
    while(1);
  }

  while(!ccs.available());
}

void dataCO2(){
  if(ccs.available()){
    if(!ccs.readData()){
      co2Value = ccs.geteCO2();
      aux = co2Str + co2Value;
      Serial.println(aux);
    }
  }
  else{
      Serial.println("ERROR:Sensor CO2 no disponible");
      delay(1000);
  }
}


// Funciones PM /////////////////////////////////////////////////////
void setupPM(){
  PMSerial.begin(9600);   
  PMSerial.setTimeout(1500);
  delay(3000);
}

void dataPM(){
  if(PMSerial.find(0x42)){    
    PMSerial.readBytes(buf,LENG);
    if(buf[0] == 0x4d){
      if(checkValue(buf,LENG)){
        PM01Value=transmitPM01(buf); 
        PM2_5Value=transmitPM2_5(buf);
        PM10Value=transmitPM10(buf); 
      }           
    } 
  }

  aux = pm1Str + PM01Value;
  Serial.println(aux);
  aux = pm25Str + PM2_5Value;
  Serial.println(aux);
  aux = pm10Str + PM10Value;
  Serial.println(aux);  
}

char checkValue(unsigned char *thebuf, char leng)
{  
  char receiveflag=0;
  int receiveSum=0;

  for(int i=0; i<(leng-2); i++){
  receiveSum=receiveSum+thebuf[i];
  }
  receiveSum=receiveSum + 0x42;
 
  if(receiveSum == ((thebuf[leng-2]<<8)+thebuf[leng-1]))  //check the serial data 
  {
    receiveSum = 0;
    receiveflag = 1;
  }
  return receiveflag;
}

int transmitPM01(unsigned char *thebuf)
{
  int PM01Val;
  PM01Val=((thebuf[3]<<8) + thebuf[4]); //count PM1.0 value of the air detector module
  return PM01Val;
}

//transmit PM Value to PC
int transmitPM2_5(unsigned char *thebuf)
{
  int PM2_5Val;
  PM2_5Val=((thebuf[5]<<8) + thebuf[6]);//count PM2.5 value of the air detector module
  return PM2_5Val;
  }

//transmit PM Value to PC
int transmitPM10(unsigned char *thebuf)
{
  int PM10Val;
  PM10Val=((thebuf[7]<<8) + thebuf[8]); //count PM10 value of the air detector module  
  return PM10Val;
}


// Funciones Light //////////////////////////////////////////////////
void dataLight(){
  lightValue = analogRead(lightPin);
  aux = lightStr + lightValue;
  Serial.println(aux);
}


// Funciones DHT //////////////////////////////////////////////////
void dataDHT(){
  tempDHValue = dht.readTemperature();
  humDHValue = dht.readHumidity();
  
  aux = humDHStr + humDHValue;
  Serial.println(aux);
  aux = tempDHStr + tempDHValue;
  Serial.println(aux);
}
