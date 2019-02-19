class Kindermann:
    port = '/dev/ttyUSB0'

    def __init__(self):
        pass

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

    def send_command(self):
        ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=115200,
            #        baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        logging.warning(ser.isOpen())

        command_hdmi1 = [0x7B, 0x7B, 0x09, 0x00, 0x02, 0x00, 0x01, 0xFC, 0x7D, 0x7D]
        command_hdmi2 = [0x7B, 0x7B, 0x09, 0x00, 0x02, 0x00, 0x02, 0xFD, 0x7D, 0x7D]
        command_vga = [0x7B, 0x7B, 0x09, 0x00, 0x02, 0x00, 0x03, 0xFE, 0x7D, 0x7D]
        command_next_input = [0x7B, 0x7B, 0x08, 0x00, 0x01, 0x00, 0xF9, 0x7D, 0x7D]

        command = command_hdmi2
        ser.write(command)
        ser.flush()
        test = ''
        while ser.in_waiting:
            test += ser.readline()
        ser.close()
        if test != '':
            logging.warning(test)