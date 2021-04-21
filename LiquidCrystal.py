import time
import machine

# LCD data sheet: https://www.sparkfun.com/datasheets/LCD/HD44780.pdf

# todo: Add some error and exception handling.
# todo: Add optional compatibility with 5x10 dots displays.
# todo: Convert commands system to work with bytes instead of strings.


class LCD:
    '''Class for convenient handling of a LCD display via parallel interface.'''

    def __init__(self,data_pins:list,EN_pin:int,RS_pin:int,RW_pin:int,lcd_size:tuple):
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
        self.__ENABLE_TIME = 1e-6  # 1000 ns as specified in LCD's data sheet.

    def initialize(self):
        '''Sets the given pins to output and initializes the display.'''

        self.data_pins = [machine.Pin(pin,machine.Pin.OUT) for pin in self.data_pins_ind]
        self.enable_pin = machine.Pin(self.enable_pin_ind,machine.Pin.OUT)
        self.select_pin = machine.Pin(self.select_pin_ind,machine.Pin.OUT)
        self.readwrite_pin = machine.Pin(self.readwrite_pin_ind,machine.Pin.OUT)

        self.__shift_command("000010")  # Set display to 4-bit operation.

        self.__shift_command("000010")
        self.__shift_command("001000")  # Set display to 2 lines, 5x8 dots digits

        self.__shift_command("000000")
        self.__shift_command("001100")  # Set cursor, turn on LCD

        self.__shift_command("000000")
        self.__shift_command("000110")  # Entry mode

        self.clear()

    def clear(self):
        '''Clears the contents of the display and moves the cursor to (0,0) point.'''

        self.__shift_command("000000")
        self.__shift_command("000001")

    def print(self,parameter):
        '''Prints the given string at current cursor position.'''

        if isinstance(parameter,str):
            for char in parameter:
                self.__print_char(char)
        else:
            address = '{:08b}'.format(parameter)
            self.__shift_command("10" + address[:4])
            self.__shift_command("10" + address[4:])

    def __print_char(self,char:str):

        bin_str = '{:08b}'.format(ord(char))
        self.__shift_command("10" + bin_str[:4])
        self.__shift_command("10" + bin_str[4:])

    def __shift_command(self,command_bits:str):  # Probably needs a rebuild to speed it up.

        time.sleep(self.__ENABLE_TIME)
        self.select_pin.value(int(command_bits[0]))
        self.readwrite_pin.value(int(command_bits[1]))

        for pin,command_bit in zip(self.data_pins,command_bits[2:]):
            pin.value(int(command_bit))

        self.enable_pin.value(1)
        time.sleep(self.__ENABLE_TIME)
        self.enable_pin.value(0)

    def set_cursor(self,coordinates:tuple,cursor_visible:bool = False,cursor_blinking:bool = False):
        '''Sets the cursor at specified position, indices start at 0.'''

        if cursor_visible and cursor_blinking:
            self.__shift_command("000000")
            self.__shift_command("001111")
        elif cursor_visible and not cursor_blinking:
            self.__shift_command("000000")
            self.__shift_command("001110")
        elif not cursor_visible and cursor_blinking:
            self.__shift_command("000000")
            self.__shift_command("001101")

        address = '{:07b}'.format(coordinates[0]*64 + coordinates[1])

        self.__shift_command("001" + address[:3])
        self.__shift_command("00" + address[3:])

    def scroll_display(self,direction:int):
        '''Moves the entire display contents by 1. dir = 1 increment, dir = -1 decrement'''

        if direction == 1:
            self.__shift_command("000001")
            self.__shift_command("001100")
        elif direction == -1:
            self.__shift_command("000001")
            self.__shift_command("001000")

    def create_char(self,address_index,char_bytes):

        CGRAM_address = '{:08b}'.format(64+address_index)

        self.__shift_command("00" + CGRAM_address[:4])
        self.__shift_command("00" + CGRAM_address[4:])  # set CGRAM adress

        for byte in char_bytes:
            self.__shift_command("10000" + byte[0])
            self.__shift_command("10" + byte[1:])

        self.set_cursor((0,0))

