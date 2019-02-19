import logging
import serial

epson_information = {
    "NORMAL": 'Normal:ASPECT 00:#A99617',
    "WIDE": 'Wide:ASPECT 20:#A99617',
    "AUTO": 'Auto:ASPECT 30:#A99617',
    "FULL": 'Full:ASPECT 40:#A99617',
    "ZOOM": 'Zoom:ASPECT 50:#A99617',
    "THROUGH": 'Through:ASPECT 60:#A99617',
    "SYNC": 'Syncing ... :KEY 4A:#A99617',
    "VGA": 'Input VGA:SOURCE 1F:#A99617',
    "HDMI1": 'Input HDMI1:SOURCE 30:#A99617',
    "HDMI2": 'Input HDM2I:SOURCE A0:#A99617',
    "HDBASET": 'Input HDBaseT:SOURCE 80:#A99617',
    "MUTE": 'Mute on:MUTE ON:#F59554',
    "MUTEOFF": 'Mute off:MUTE OFF:#F59554',
    "VOLOFF": 'Audio off:VOL 0:#F00000',
    "VOL1": 'Audio  1:VOL 1:#F5BCA9',
    "VOL2": 'Audio  2:VOL 2:#F5BCA9',
    "VOL3": 'Audio  3:VOL 3:#F5BCA9',
    "VOL4": 'Audio  4:VOL 4:#F5BCA9',
    "VOL5": 'Audio  5:VOL 5:#F5BCA9',
    "VOL6": 'Audio  6:VOL 6:#F5BCA9',
    "VOL7": 'Audio  7:VOL 7:#F5BCA9',
    "VOL8": 'Audio  8:VOL 8:#F5BCA9',
    "VOL9": 'Audio  9:VOL 9:#F5BCA9',
    "VOLDEF": 'Audio default:VOL 10:#74DF00',
    "VOL11": 'Audio 11:VOL 11:#F5BCA9',
    "VOL12": 'Audio 12:VOL 12:#F5BCA9',
    "VOL13": 'Audio 13:VOL 13:#F5BCA9',
    "VOL14": 'Audio 14:VOL 14:#F5BCA9',
    "VOL15": 'Audio 15:VOL 15:#F5BCA9',
    "VOL16": 'Audio 16:VOL 16:#F5BCA9',
    "VOL17": 'Audio 17:VOL 17:#F5BCA9',
    "VOL18": 'Audio 18:VOL 18:#F5BCA9',
    "VOL19": 'Audio 19:VOL 19:#F5BCA9',
    "VOLMAX": 'Audio max:VOL 20:#F00000',
    "ON": 'Beamer on:PWR ON:#00A000',
    "OFF": 'Beamer off:PWR OFF:#F00000'
}


class Epson:

    def __init__(self, baudrate=9600, tty_port='/dev/ttyUSB0'):
        self.baudrate = baudrate
        self.port = tty_port

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
        test = ''
        while ser.in_waiting:
            test += ser.readline()
        ser.close()
        if test != '':
            logging.warning(test)

    @staticmethod
    def _get_bytearray_command(key):
        s = epson_information[key].split(':')[1]
        b = bytearray()
        b.extend(map(ord, s))
        b.extend(map(ord, '\r\n'))
        return b
