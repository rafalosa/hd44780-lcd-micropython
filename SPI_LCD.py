import machine
import time


class SPILCD:

    def __init__(self,data_pins,EN_pin,RS_pin,RW_pin,lcd_size):
        self.data_pins_ind = data_pins
        self.enable_pin_ind = EN_pin
        self.select_pin_ind = RS_pin
        self.readwrite_pin_ind = RW_pin
        self.rows = lcd_size[0]
        self.columns = lcd_size[1]
        self.data_pins = None
        self.enable_pin = None
        self.select_pin = None
        self.readwrite_pin = None
        self.__ENABLE_TIME = 1e-5

    def initialize(self):

        self.data_pins = [machine.Pin(pin,machine.Pin.OUT) for pin in self.data_pins_ind]
        self.enable_pin = machine.Pin(self.enable_pin_ind,machine.Pin.OUT)
        self.select_pin = machine.Pin(self.select_pin_ind,machine.Pin.OUT)
        self.readwrite_pin = machine.Pin(self.readwrite_pin_ind,machine.Pin.OUT)

        self.__shift_command("000010")  # Set display to 4-bit operation.
        self.__shift_command("001000")  # Set display to 2 lines, 5x8 dots digits

        self.__shift_command("000000")
        self.__shift_command("001111")  # Set cursor

        self.__shift_command("000000")
        self.__shift_command("000110")  # Entry mode

        self.__shift_command("000000")
        self.__shift_command("000010")  # Return home

    def clear(self):

        self.__shift_command("000000")
        self.__shift_command("000001")

    def print(self,string):

        self.__shift_command("100100")
        self.__shift_command("101000")

    def __shift_command(self,command_bits):

        self.select_pin.value(int(command_bits[0]))
        self.readwrite_pin.value(int(command_bits[1]))

        for pin,command_bit in zip(self.data_pins,command_bits[2:]):
            pin.value(int(command_bit))

        self.enable_pin.value(1)
        time.sleep(self.__ENABLE_TIME)
        self.enable_pin.value(0)