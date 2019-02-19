#!/usr/bin/python3
import cgi
import os
from time import localtime, strftime

from epson.epson import Epson
from kindermann.kindermann import Kindermann

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
    "HDMI2": 'Input HDMI2:SOURCE A0:#A99617',
    "HDBASET": 'Input HDBaseT:SOURCE 80:#A99617',
    "MUTE": 'Mute ON:MUTE ON:#F59554',
    "MUTEOFF": 'Mute OFF:MUTE OFF:#F59554',
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

kindermann_commands = ['ON', 'HDMI1', 'HDMI2', 'VGA']


def get_html(key):
    # Rueckmeldung an rufende Seite
    time = strftime('%H:%M:%S', localtime())
    color = get_color(key)
    message = get_message(key)
    return '<font size="3">Last Action at {}</font>' \
           '<br><font size="5" color="{}">{}</font>'.format(time, color, message)


def get_color(key):
    return epson_information[key].split(':')[2]


def get_message(key):
    return epson_information[key].split(':')[0]


def toggle_mute(on=False):
    mutefile = './mutefile'

    if on and os.path.isfile(mutefile):
        # if beamer is switched on we have to delete the old mute status
        os.remove(mutefile)
        return

    if not os.path.isfile(mutefile):
        with open(mutefile, "w+") as file:
            file.write('this is a tmp_file')
        return False
    else:
        os.remove(mutefile)
        return True


def execute_funktion(key):
    epson = Epson()
    kindermann = Kindermann()

    if key not in kindermann_commands:
        if key == 'MUTE':
            if not toggle_mute():
                # if not toggle_mute, the projector is already in mute and has to be unmuted
                key = 'MUTEOFF'
        epson.send_command(key)
    else:
        if key == 'ON':
            toggle_mute(on=True)  # delete old status of the mute command
            kindermann.send_command('SHOW_ME')
            epson.send_command('ON')
            epson.send_command('ON')
            epson.send_command('ON')
            epson.send_command('ON')
            epson.send_command('ON')
            epson.send_command('ON')
            epson.send_command('HDBASET')
        else:
            kindermann.send_command(key)
            epson.send_command('HDBASET')
    print(get_html(key))


print("Content-Type: text/html")  # HTML is following
print()
arguments = cgi.FieldStorage()
if 'Funktion' in arguments:
    value = arguments['Funktion'].value
    execute_funktion(value)
