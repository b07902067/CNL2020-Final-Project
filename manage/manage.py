#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import secrets
import hmac
from datetime import datetime

ID_FILE_PREFIX="./ID_FILES/"

def genKEY():
    # bytes to hex string
    return secrets.token_bytes(8).hex()
    # hex string to bytes : bytes.fromhex(hexstring)

def computeIDs(key_for_ID, msg_for_ID):
    return hmac.new(key_for_ID,msg=msg_for_ID.encode(),digestmod='SHA256').hexdigest()
    
# def sendIDs():


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        print(self.path[8:])
        if self.path == "/getkey":
            KEY = genKEY()
            self.wfile.write("KEY={}\n".format(KEY).encode('utf-8'))
            self.wfile.write("Have a nice day\n".encode('utf-8'))
        elif self.path[:8] == "/checkid":
            try:
                with open(ID_FILE_PREFIX+self.path[8:], "r") as f:
                    for i in f.readlines():
                        self.wfile.write(i.encode('utf-8'))
            except FileNotFoundError:
                self.wfile.write("NO SUCH PATH".encode('utf-8'))
        else :
            self.wfile.write("Wear mask!!\n".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        key_list = post_data.decode('utf-8').split('&')
        for i in key_list:
            date_ = i.split("=")[0]
            key_ = i.split("=")[1]
            with open(ID_FILE_PREFIX+date_, "a") as f:
                for j in range(0, 24):
                    f.write(computeIDs(bytes.fromhex(key_), date_+"-"+str(j))+"\n")
                    print(computeIDs(bytes.fromhex(key_), date_+"-"+str(j)))

        self._set_response()
        self.wfile.write("Hope you get well soon!!".encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()