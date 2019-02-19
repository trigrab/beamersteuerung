from kindermann.kindermann import Kindermann
from epson.epson import Epson

if __name__ == '__main__':
    kman = Kindermann()
    kman.send_command('vga')
    epson = Epson()
    epson.send_command('ON')
