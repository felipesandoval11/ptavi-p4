#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Made by Felipe Sandoval Sibada
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
LINE = ' '.join(sys.argv[3:])

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
if __name__ == "__main__":
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
            my_socket.connect((SERVER, PORT))
            print("Enviando:", LINE)
            my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
            data = my_socket.recv(1024)
            print('Recibido -- ', data.decode('utf-8'))

        print("Socket terminado.")
    except IncompleteError:
        print("Usage: python3 client.py ip port line")
        
