import serial
import logging

commands = {
    'HDMI1': [0x7B, 0x7B, 0x09, 0x00, 0x02, 0x00, 0x01, 0xFC, 0x7D, 0x7D],
    'HDMI2': [0x7B, 0x7B, 0x09, 0x00, 0x02, 0x00, 0x02, 0xFD, 0x7D, 0x7D],
    'VGA': [0x7B, 0x7B, 0x09, 0x00, 0x02, 0x00, 0x03, 0xFE, 0x7D, 0x7D],
    'SHOW_ME': [0x7B, 0x7B, 0x08, 0x00, 0x01, 0x00, 0xF9, 0x7D, 0x7D],
    'power_on': [0x7B, 0x7B, 0x13, 0x00, 0x02, 0xFF, 0x00, 0x04, 0x7D, 0x7D],
}


class Kindermann:
    def __init__(self, baudrate=115200, tty_port='/dev/ttyUSB0'):
        self.baudrate = baudrate
        self.port = tty_port

    def set_baudrate(self, current_baudrate=115200, baudrate=9600):
        ser = serial.Serial(
            port=self.port,
            baudrate=current_baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

        baudrates = {
            110: 0x00,
            300: 0x01,
            600: 0x02,
            1200: 0x03,
            2400: 0x04,
            4800: 0x05,
            9600: 0x06,
            14400: 0x07,
            19200: 0x08,
            38400: 0x09,
            56000: 0x0A,
            57600: 0x0B,
            115200: 0x0C,
        }

        if baudrate in baudrates:
            baudrate = baudrates[baudrate]
        else:
            raise Exception('Serial Port not supported')

        command_set_baud = [0x7B, 0x7B, 0x16, 0x00, 0x02, 0xFF, baudrate, 0x7D, 0x7D]
        ser.write(command_set_baud)
        ser.flush()
        ser.close()

    def send_command(self, key):
        ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        logging.warning(ser.isOpen())

        command = commands[key]
        ser.write(command)
        ser.flush()
        ser.close()
