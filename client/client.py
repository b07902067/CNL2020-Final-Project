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
ID_FILE_PREFIX="./ID_FILES/"

''' Server Information'''
Server_IP="127.0.0.1"
Server_PORT=8080
Server_ADDR="http://{}:{}".format(Server_IP, str(Server_PORT))
# print(Server_ADDR)


def computeID(key_for_ID, msg_for_ID):
    return hmac.new(key_for_ID,msg=msg_for_ID.encode(),digestmod='SHA256').hexdigest()

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
        interval = datetime.now() - datetime(int(d[0]), int(d[1]), int(d[2]))
        if interval.days > 14:
            del KEYS[key_]
    # save the key dictionary
    with open(KEY_FILE_PATH, 'wb') as handler:
            pickle.dump(KEYS, handler)

''' communicate with management server '''
def reqKEY():
    while True:
        r = requests.get(Server_ADDR+"/getkey")
        if r.status_code == requests.codes.ok:
            print(r.text)
            key_now=r.text.split()[0][4:]
            date_now = datetime.now().date().strftime("%Y-%m-%d")
            saveKEY(date_now, key_now)
            break

def sendKEY():
    if os.path.isfile(KEY_FILE_PATH):
        with open(KEY_FILE_PATH, 'rb') as handler:
            KEYS = pickle.load(handler)
    for key_ in KEYS:
        d = key_.split('-')
        interval = datetime.now() - datetime(int(d[0]), int(d[1]), int(d[2]))
        if interval.days > 14:
            del KEYS[key_]
    while True:
        r = requests.post(Server_ADDR, data=KEYS)
        if r.status_code == requests.codes.ok:
            print(r.text)
            break

def checkID():
    for i in os.listdir(ID_FILE_PREFIX):
        r = requests.get(Server_ADDR+"/checkid/"+i)
        print("pre")
        if r.status_code == requests.codes.ok:
            print("text", r.text)
            if r.text[:1] == "NO":
                continue
            else :
                positive_ID_list = r.text.split("\n")
                with open(ID_FILE_PREFIX+i, "r") as f:
                    local_ID_list = f.readlines()
                    for pid in positive_ID_list:
                        for lid in local_ID_list:
                            if pid == lid[:-1]:
                                return True
    return False


''' communicate with AP server '''
# def sendID():
# def recvID():

''' communicate with DB '''
# def saveID():


if __name__ == '__main__':
    # reqKEY()
    # for key in KEYS:
    #     print("my ID is ", computeID(bytes.fromhex(KEYS[key]), key))
    # sendKEY()
    print(checkID())
