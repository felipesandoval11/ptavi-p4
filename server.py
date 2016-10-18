#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Made by Felipe Sandoval Sibada
"""Programa servidor UDP que abre un socket a un servidor."""

import socketserver
import sys


# Constantes. Dirección IP del servidor y contenido a enviar
class EchoHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        self.wfile.write(b"Hemos recibido tu peticion")
        for line in self.rfile:
            print("IP cliente: " + str(self.client_address[0]) +
                  " | puerto: " + str(self.client_address[1]))
            print("El cliente nos manda ", line.decode('utf-8'))

if __name__ == "__main__":
    try:
        serv = socketserver.UDPServer(('', int(sys.argv[1])), EchoHandler)
        print("Lanzando servidor UDP de eco...")
        serv.serve_forever()
    except IndexError:
        print("Usage: python3 server.py port")
    except KeyboardInterrupt:
        print("Finalizado servidor")
