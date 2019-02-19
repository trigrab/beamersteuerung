#!/usr/local/bin/python3
import cgi
from epson.epson import Epson

print("Content-Type: text/html")    # HTML is following
print()
print("<TITLE>CGI script output</TITLE>")
print("<H1>This is my first CGI script</H1>")
arguments = cgi.FieldStorage()
if 'Funktion' in arguments:
        epson = Epson()
        epson.send_command(arguments['Funktion'])

for i in arguments.keys():
        print(arguments[i].value)
