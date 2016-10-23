#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Made by Felipe Sandoval Sibada
"""Programa cliente UDP que abre un socket a un servidor."""

import socket
import sys

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    LINE = ' '.join(sys.argv[3:])
    if len(sys.argv) != 6 or not str.isdigit(sys.argv[5]):
        raise IndexError
except IndexError:
    sys.exit("Usage: client.py ip puerto REGISTER sip_address expires_value")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
if __name__ == "__main__":
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
            my_socket.connect((SERVER, PORT))
            print(sys.argv[3] + " " + sys.argv[4], "SIP/2.0\r\n" +
                  "Expires: " + sys.argv[5], "\r\n\r\n")
            my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
            data = my_socket.recv(1024)
            print('--', data.decode('utf-8'))
            print("Socket terminado.")
    except ConnectionRefusedError:
        print("No es posible establecer la conexion. Servidor no encontrado.")
