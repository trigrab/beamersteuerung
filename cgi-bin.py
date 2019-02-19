#!/usr/bin/python3
import cgi
import os
from time import localtime, strftime

from epson.epson import Epson, epson_information
from kindermann.kindermann import Kindermann

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

    if on:
        if os.path.isfile(mutefile):
            # if beamer is switched on we have to delete the old mute status
            os.remove(mutefile)
        return

    if not os.path.isfile(mutefile):
        with open(mutefile, "w+") as file:
            file.write('this is a tmp_file')
        return True
    else:
        os.remove(mutefile)
        return False


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
