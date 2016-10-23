#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Made by Felipe Sandoval Sibada
"""Clase (y programa principal) para un servidor de eco en UDP simple"""

import socketserver
import json
import datetime
import time
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """Defino mi variable my_dic como atributo de clase."""

    my_clients = []

    def json2registered(self):
        try:
            with open("registered.json", "r") as data_file:
                loaded = json.load(data_file)
                loaded.append(self.my_clients)
            return True
        except:
            return False

    def register2json(self):
        if not self.json2registered():  # Primero que escribo.
            with open("registered.json", "w") as outfile:
                json.dump(self.my_clients,  outfile, indent=4,
                          sort_keys=True, separators=(',', ':'))
        else:                           # Al momento de actualizar.
            with open("registered.json", "w") as outfile:
                json.dump(self.my_clients,  outfile, indent=4,
                          sort_keys=True, separators=(',', ':'))

    def handle(self):
        """Handler que se ejecuta cada vez que se reciba un mensaje."""
        found = False
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        print("IP cliente: " + str(self.client_address[0]),
              "| puerto: " + str(self.client_address[1]), '\n')
        for line in self.rfile:
            line_str = str(line.decode('utf-8'))
            sip_addr = line_str.split(' ')[1]
            time_exp = int(line_str.split(' ')[2])
            time_to_del = time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.gmtime(time.time() + time_exp))
            print(line_str)
        if line_str.split(' ')[0].isupper()\
           and line_str.split(' ')[0] == "REGISTER":
            my_user = [sip_addr, {"address": str(self.client_address[0]),
                       "expires": time_to_del}]
            if time_exp != 0:
                for client in self.my_clients:
                    if client[0] == my_user[0]:
                        client[1] = my_user[1]
                        found = True
                if not found:
                    self.my_clients.append(my_user)
            else:
                for client in self.my_clients:
                    if client[0] == my_user[0]:
                        self.my_clients.remove(client)
        self.expired()
        self.register2json()
    
    def expired(self):
        actual_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.gmtime(time.time()))
        for client in self.my_clients:
            if client[1]["expires"] < actual_time:
                self.my_clients.remove(client)
        return self.my_clients
        

if __name__ == "__main__":
    try:
        serv = socketserver.UDPServer(('', int(sys.argv[1])),
                                      SIPRegisterHandler)
        print("Lanzando servidor UDP de eco...")
        serv.serve_forever()
    except IndexError:
        sys.exit("Usage: python3 server.py port")
    except KeyboardInterrupt:
        print("Finalizado servidor")