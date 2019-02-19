#!/usr/local/bin/python3
import cgi

print("Content-Type: text/html")    # HTML is following
print()
print("<TITLE>CGI script output</TITLE>")
print("<H1>This is my first CGI script</H1>")
arguments = cgi.FieldStorage()
for i in arguments.keys():
        print(arguments[i].value)
