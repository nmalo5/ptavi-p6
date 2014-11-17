#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os

comandos = sys.argv


SERVER = comandos[1]
PORT = int(comandos[2])
FICH_AUDIO = comandos[3]


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        while 1:
            line = self.rfile.read()
            print "El cliente nos manda " + line
            lista = line.split(" ")
            metodo = lista[0]
            metodos = ['INVITE', 'ACK', 'BYE']

            if not line:
                break

            if metodo == "INVITE":
                respuesta = "SIP/2.0 100 Trying\r\n\r\n"
                respuesta += "SIP/2.0 180 Ring\r\n\r\n"
                respuesta += "SIP/2.0 200 OK\r\n\r\n"
                self.wfile.write(respuesta)
            elif metodo == "ACK":
                aEjecutar = './mp32rtp -i 127.0.0.1 -p 230321 <' + FICH_AUDIO
                os.system('chmod 755 mp32rtp')                
                os.system(aEjecutar)
            elif metodo == "BYE":
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            elif not metodo in metodos:
                self.wfile.write("SIP/2.0 405 Method Not Allowed\r\n\r\n")
            else:
                self.wfile.write("SIP/2.0 400 Bad\r\n\r\n")

if __name__ == "__main__":
    if len(comandos) != 4:
        print "Usage: python server.py IP port audio_file"
    serv = SocketServer.UDPServer((SERVER, PORT), EchoHandler)
    print "Listening..."
    serv.serve_forever()
