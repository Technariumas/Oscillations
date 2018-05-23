#include<Wire.h>
const int MPU_addr = 0x68; // I2C address of the MPU-6050
int16_t AcX, AcY, AcZ;
unsigned long previousMillis = 0;        
const int interval = 5;           
const long startupTime = 60000;

 

void setup() {
    while (millis() < startupTime) {
          }  
  Wire.setSDA(8);
  Wire.setSCL(7);
  Wire.begin();
  Wire.setClock(400000L);
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  Serial.begin(115200);
}
void loop() {
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
     Wire.requestFrom(MPU_addr, 14, true); // request a total of 14 registers
    AcX = Wire.read() << 8 | Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
    AcY = Wire.read() << 8 | Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
    AcZ = Wire.read() << 8 | Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
    Serial.print(micros());
    Serial.print(",");
    Serial.print(AcX);
    Serial.print(","); Serial.print(AcY);
    Serial.print(","); Serial.println(AcZ);
}
}