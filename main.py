import SPI_LCD as sl
import time

print("Entered main.py")
LCD = sl.SPILCD([16,5,3,4],12,14,13,(2,16))
print("Created LCD object")
LCD.initialize()
print("Initialization ended")

for i in range(5):
    LCD.print("o")
    time.sleep(1)
    print(i)