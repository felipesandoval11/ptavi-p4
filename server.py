#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Made by Felipe Sandoval Sibada
"""Programa servidor UDP que abre un socket a un servidor."""

import socketserver
import json
import datetime
import time
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """Defino mi variable my_dic como atributo de clase."""

    my_dic = {}
    my_user = []
    
    def json2registered(self):
        try:
            with open("registered.json", "r") as data_file:
                data = json.load(data_file)
            return data
        except FileNotFoundError:
            return False
        
    
    def register2json(self):
        if not self.json2registered():
            with open("registered.json", "w") as outfile:
                json.dump([self.my_user],  outfile, indent=4, sort_keys=True,
                          separators=(',', ':'))
            print("escribo primero")
        else:
            print("actualizo yes")

    def handle(self):
        """Handler que se ejecuta cada vez que se reciba un mensaje."""
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        print("IP cliente: " + str(self.client_address[0]) +
              " | puerto: " + str(self.client_address[1]) + '\n')
        for line in self.rfile:
            line_str = str(line.decode('utf-8'))
            sip_addr = line_str.split(' ')[1]
            time_exp = int(line_str.split(' ')[2])
            time_to_del = time.strftime("%Y-%m-%d %H:%M:%S",
                          time.gmtime(time.time() + time_exp))
            print("El cliente nos manda ", line_str)
            if line_str.split(' ')[0].isupper()\
               and line_str.split(' ')[0] == "REGISTER":
                self.my_dic = {"address":str(self.client_address[0]),\
                               "expires":time_to_del}
                self.my_user = [sip_addr, self.my_dic]
                if time_exp == 0:
                    del self.my_dic["address", "expires"]
        self.register2json()

if __name__ == "__main__":
    try:
        serv = socketserver.UDPServer(('', int(sys.argv[1])),
                                      SIPRegisterHandler)
        print("Lanzando servidor UDP de eco...")
        serv.serve_forever()
    except IndexError:
        print("Usage: python3 server.py port")
    except KeyboardInterrupt:
        print("Finalizado servidor")
