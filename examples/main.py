import SPI_LCD as sl
import time
# Tested on ESP8266

time.sleep(2)
LCD = sl.SPILCD([16,5,2,4],12,14,13,(2,16))
LCD.initialize()
LCD.print("Hello world!")