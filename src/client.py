from typing import Text
import requests
import time
import pickle
from datetime import datetime
import os
import hmac

KEYS={}

''' File Path '''
KEY_FILE_PATH="./KEY_FILE"

''' Server Information'''
Server_IP="127.0.0.1"
Server_PORT=8080
Server_ADDR="http://{}:{}".format(Server_IP, str(Server_PORT))
# print(Server_ADDR)

''' save KEY or ID '''
def saveKEY(date_now, key_now):
    global KEYS

    # load keys if key file exists
    if os.path.isfile(KEY_FILE_PATH):
        with open(KEY_FILE_PATH, 'rb') as handler:
            KEYS = pickle.load(handler)
    
    # check if this client has gotten key today
    if not date_now in KEYS:
        KEYS[date_now] = key_now
        print("Got key!\n")
    else :
        print("You've gotten key today!\n")
    
    # remove keys if 14 days have passed
    for key_ in KEYS:
        d = key_.split('-')
        interval = datetime.now() - datetime(d[0], d[1], d[2])
        if interval.days > 14:
            del KEYS[key_]
    # save the key dictionary
    with open(KEY_FILE_PATH, 'wb') as handler:
            pickle.dump(KEYS, handler)

''' communicate with management server '''
def reqKEY():
    while True:
        r = requests.get(Server_ADDR+"/getkey")
        newKEY=""
        if r.status_code == requests.codes.ok:
            print(r.text)
            key_now=r.text.split()[0][4:]
            date_now = datetime.now().date().strftime("%Y-%m-%d")
            saveKEY(date_now, key_now)
            break

def sendKEY():
    r = requests.post(Server_ADDR, data=KEYS)
    print(r.text)
# def checkID():

''' communicate with AP server '''
# def computeID():
# def sendID():
# def recvID():

''' communicate with DB '''
# def saveID():


reqKEY()
sendKEY()
# r = requests.post("http://bugs.python.org", data={'number': 12524, 'type': 'issue', 'action': 'show'})
# print(r.status_code, r.reason)
# print(r.text[:300] + '...')