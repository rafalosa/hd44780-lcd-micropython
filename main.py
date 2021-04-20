import SPI_LCD as sl
import time

time.sleep(5)
print("zaczynam")

LCD = sl.SPILCD([16,5,2,4],12,14,13,(2,16))
print("1")
LCD.initialize()
print("3")
LCD.print('o')
print("2")