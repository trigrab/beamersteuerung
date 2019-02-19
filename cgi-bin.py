#!/usr/bin/python3
import cgi
from epson.epson import Epson
from kindermann.kindermann import Kindermann

kindermann_commands = ['ON', 'HDMI1', 'HDMI2', 'VGA']

print("Content-Type: text/html")  # HTML is following
print()
print("<TITLE>CGI script output</TITLE>")
print("<H1>This is my first CGI script</H1>")
arguments = cgi.FieldStorage()
if 'Funktion' in arguments:
    value = arguments['Funktion'].value
    epson = Epson()
    kindermann = Kindermann()

    if value not in kindermann_commands:

        epson.send_command(arguments['Funktion'].value)
    else:
        if value == 'ON':
            kindermann.send_command('SHOW_ME')
            epson.send_command('ON')
            epson.send_command('ON')
            epson.send_command('ON')
            epson.send_command('ON')
            epson.send_command('ON')
            epson.send_command('ON')
            epson.send_command('HDBASET')
        else:
            kindermann.send_command(value)
            epson.send_command('HDBASET')

for i in arguments.keys():
    print(arguments[i].value)
