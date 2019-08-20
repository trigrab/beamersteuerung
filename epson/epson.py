import logging
from importlib import import_module

import serial

try:
    from config import epson_config_file_name
except ImportError:
    epson_config_file_name = 'epson_default_config'

try:
    from config import epson_config_varname
except ImportError:
    epson_config_varname = 'epson_default'

class Epson:

    def __init__(self, baudrate=9600, tty_port='/dev/ttyUSB0'):
        self.baudrate = baudrate
        self.port = tty_port
        epson_config = import_module('epson.' + epson_config_file_name)
        self.epson_information = getattr(epson_config, epson_config_varname)

    def send_command(self, key):
        ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        logging.warning(ser.isOpen())

        command = self._get_bytearray_command(key)
        ser.write(command)

        ser.flush()
        ser.close()

    def _get_bytearray_command(self, key):
        s = self.epson_information[key].split(':')[1]
        b = bytearray()
        b.extend(map(ord, s))
        b.extend(map(ord, '\r\n'))
        return b
