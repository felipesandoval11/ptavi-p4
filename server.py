#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Made by Felipe Sandoval Sibada
"""Class and main program for a echo server of UDP-SIP."""

import socketserver
import json
import datetime
import time
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """Main handler that use a Dict to save all info."""

    my_dic = {}         # Diccionario de clientes para gestionar.
    exist_file = True

    def json2registered(self):
        """Method to look if there is an over-existing json file."""
        try:
            with open("registered.json", "r") as data_file:
                self.my_dic = json.load(data_file)
                self.exist_file = True
        except:
            self.exist_file = False

    def register2json(self):
        """Method to write a json file of my_dic."""
        if not self.exist_file or len(self.my_dic) == 0:
            with open("registered.json", "w") as outfile:
                json.dump(self.my_dic,  outfile, indent=4, sort_keys=True,
                          separators=(',', ':'))
        else:
            with open("registered.json", "r+") as outfile:
                json.dump(self.my_dic,  outfile, indent=4, sort_keys=True,
                          separators=(',', ':'))

    def handle(self):
        """Handler to manage incoming users SIP request."""
        found = False
        print("IP:" + str(self.client_address[0]),
              "| PORT: " + str(self.client_address[1]), '\n')
        line_str = self.rfile.read().decode('utf-8')
        sip_addr = line_str.split(' ')[1][4:]
        time_exp = int(line_str.split(' ')[3])
        time_to_del = time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.gmtime(time.time() + time_exp))
        print(line_str)
        if line_str.split(' ')[0].isupper() and\
           line_str.split(' ')[0] == "REGISTER":
            self.json2registered()
            self.my_dic[sip_addr] = {"address": str(self.client_address[0]),
                                     "expires": time_to_del}
            if time_exp == 0:
                del self.my_dic[sip_addr]
            self.expired()
            self.register2json()
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

    def expired(self):
        """Method that checks if there's an old client in my_dic."""
        actual_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.gmtime(time.time()))
        expired_dic = []
        for client in self.my_dic:
            if self.my_dic[client]["expires"] < actual_time:
                expired_dic.append(client)
        for client in expired_dic:
            del self.my_dic[client]
        return self.my_dic


if __name__ == "__main__":
    try:
        serv = socketserver.UDPServer(('', int(sys.argv[1])),
                                      SIPRegisterHandler)
        print("Lauching UDP echo server...")
        serv.serve_forever()
    except IndexError:
        sys.exit("Usage: python3 server.py port")
    except KeyboardInterrupt:
        print("END OF SERVER")
