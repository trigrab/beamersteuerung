#!/usr/bin/python3
import cgi
import os
from datetime import timedelta

from config import *

from time import localtime, strftime
from epson.epson import Epson, epson_information
from kindermann.kindermann import Kindermann

kindermann_commands = ['ON',
                       'HDMI1',
                       'HDMI2',
                       'VGA'
                       ]  # commands that aren't only executed by epson


def get_html(key):
    """
    get html code which will be returned to the controlling website
    :param key: used function
    :return: html code
    """
    if key == 'COOL_DOWN':
        time_since_cooldown = os.path.getctime(cool_down_file) - localtime()
        return '<font size="5" color="#FF0000">' \
               'Still cooling for {} seconds ...</font>'.format(time_since_cooldown)
    else:
        # Rueckmeldung an rufende Seite
        current_time = strftime('%H:%M:%S', localtime())
        color = get_color(key)
        message = get_message(key)
        return '<font size="3">Last Action at {}</font>' \
               '<br><font size="5" color="{}">{}</font>'.format(current_time, color, message)


def get_color(key):
    """
    get color code for html page
    :param key: used function
    :return:  html color code as str
    """
    return epson_information[key].split(':')[2]


def get_message(key):
    """
    get message for html page
    :param key: used function
    :return: message as str
    """
    return epson_information[key].split(':')[0]


def projector_muted(on=False):
    """
    checks if projector is in muted state and needs to be unmuted
    :param on: only deletes mutefile if set
    :return: if projector is in muted state
    """
    if on:
        if os.path.isfile(mutefile):
            # if beamer is switched on we have to delete the old mute status
            os.remove(mutefile)
        return False

    if not os.path.isfile(mutefile):
        with open(mutefile, "w+") as file:
            file.write('this is a tmp_file')
        return True
    else:
        os.remove(mutefile)
        return False


def projector_cooling_down():
    """
    Should the projector be switched on with notice to the cool down setting (cool_down_time)
    :return: True if projector can be switched on
    """
    if os.path.isfile(cool_down_file):
        if os.path.getctime(cool_down_file) + timedelta(seconds=coold_down_time) > localtime():
            # projector was cooling down, but does not have to cool down any more
            os.remove(cool_down_file)
            return False
        else:
            # projector is cooling down
            return True
    else:
        # projector is not cooling down
        return False


def switch_projector_on(epson, kindermann):
    """
    switches projector on with respect to cool down times set in config
    :param epson: instance of epson class
    :param kindermann: instance of kindermann class
    :return: if projector is switched on
    """
    if projector_cooling_down():
        return False
    else:
        projector_muted(on=True)  # delete old status of the mute command
        kindermann.send_command('SHOW_ME')
        epson.send_command('ON')  # directly after kindermann is switched on, we need to send
        epson.send_command('ON')  # this command multiple time to epson, otherwise it will
        epson.send_command('ON')  # not be executed.
        epson.send_command('ON')
        epson.send_command('ON')
        epson.send_command('ON')
        epson.send_command('HDBASET')
        return True


def execute_funktion(key):
    """
    executes the function given by key
    :param key: function from controlling website
    :return: None
    """
    epson = Epson(baudrate=epson_baud, tty_port=tty_port)
    kindermann = Kindermann(baudrate=kindermann_baud, tty_port=tty_port)

    if key not in kindermann_commands:
        if key == 'MUTE':
            if not projector_muted():
                # if not toggle_mute, the projector is already in mute and has to be unmuted
                key = 'MUTEOFF'
        epson.send_command(key)
    else:
        if key == 'ON':
            switched_on = switch_projector_on(epson, kindermann)
            if not switched_on:
                key = 'COOL_DOWN'
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
