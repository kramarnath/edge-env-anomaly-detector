import time 
import dht 
from machine import I2C, Pin 
from machine_i2c_lcd import I2cLcd 
from anomaly_detector import StatisticalAnomalyDetector 
 
# 1. Hardware Setup (ESP32: SDA=GPIO21, SCL=GPIO22 | ESP-12E: SDA=GPIO12, SCL=GPIO13) 
dht_sensor = dht.DHT11(Pin(4)) 
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = I2cLcd(i2c, 0x27, 2, 16) 

# Siren / Alert Output
siren = Pin(16, Pin.OUT)
siren.value(0)
 
# 2. Initialize Anomaly Detector 
detector = StatisticalAnomalyDetector() 
 
# Startup Message 
lcd.clear() 
lcd.putstr("Edge System\nInitializing...") 
time.sleep(3) 
 
while True: 
    try: 
        # Read DHT11 Sensor 
        dht_sensor.measure() 
        temp = dht_sensor.temperature() 
        humi = dht_sensor.humidity() 
 
        # Evaluate against statistical limits 
        result = detector.evaluate(temp, humi) 
        status = result["status"] 
        reasons = result["reasons"] 
 
        lcd.clear() 
 
        if status == "NORMAL": 
            # Siren OFF when readings are normal
            siren.value(0)

            # Line 1: Live Sensor Readings 
            # Line 2: Normal status 
            lcd.putstr(f"T:{temp:2d}C   H:{humi:2d}%\nStatus: Normal") 
 
        else: 
            # Siren ON when anomaly is detected
            siren.value(1)

            # Line 1: Anomaly Warning 
            # Line 2: Specific Boundary Exceeded 
            if len(reasons) > 1 and "Temp" in reasons[0] and "Humi" in reasons[1]: 
                detail = "Temp & Humi Ex" 
            else: 
                detail = reasons[0] 
 
            lcd.putstr(f"ANOMALY DETECTED\n{detail}") 
 
    except OSError: 
        # DHT11 read failure fallback 
        siren.value(0)
        lcd.clear() 
        lcd.putstr("Sensor Read Fail\nRetrying...") 
 
    time.sleep(3)