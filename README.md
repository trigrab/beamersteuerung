# beamersteuerung
Projector controller for an epson projector with a kindermann hd-base box

## steps to use this with apache cgi

1. copy this folder to your cgi-bin folder and give apache the rights to execute 
   cgi-bin.py
2. copy `config.py.dist` to config.py and change the values to suit your expectations
3. configure your website to use cgi-bin.py like
`http://localhost/cgi-bin/beamersteuerung/cgi-bin.py?Funktion=ON`