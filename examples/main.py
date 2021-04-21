import LiquidCrystal as LC
import time
# Tested on ESP8266

sample = ["01110","01010","00100","01110","10101","00100","01010","01010"]

LCD = LC.LCD([16,5,2,4],12,14,13,(2,16))
LCD.initialize()
LCD.create_char(0,sample)
LCD.clear()
LCD.print("Hello world!")
LCD.print(0)