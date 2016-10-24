#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Made by Felipe Sandoval Sibada
"""UDP Client Program that sends a SIP register request."""

import socket
import sys

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    LINE = ' '.join(sys.argv[3:])
    if len(sys.argv) != 6 or not str.isdigit(sys.argv[5]):
        raise IndexError
except (IndexError, ValueError):
    sys.exit("Usage: client.py ip puerto REGISTER sip_address expires_value")

# Creating and configuring the socket. Then we bind it to a server/port.
if __name__ == "__main__":
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
            my_socket.connect((SERVER, PORT))
            sip_str = sys.argv[3] + " sip:" + sys.argv[4] +\
                " SIP/2.0\r\n" + "Expires: " + sys.argv[5] + "\r\n"
            print(sip_str + "\r\n")
            my_socket.send(bytes(sip_str, 'utf-8') + b'\r\n')
            data = my_socket.recv(1024)
            print('-- RECIEVED SIP INFO --\n', data.decode('utf-8'))
            print("END OF SOCKET")
    except ConnectionRefusedError:
        print("Connection Refused. Server not found.")
