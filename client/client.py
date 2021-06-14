from typing import Text
import requests
import time
import pickle
from datetime import datetime
import os
import hmac
import socket
from netifaces import interfaces, ifaddresses, AF_INET
import secrets
import time

KEYS={}

''' File Path '''
KEY_FILE_PATH="./KEY_FILE"
ID_FILE_PREFIX="./ID_FILES/"

APIP = ""
def writedata(data, myID):
    datas = data.split(" ")
    with open(ID_FILE_PREFIX + datetime.now().date().strftime("%Y-%m-%d"), "a") as f:
        for i in datas:
            if i == myID:
                continue
            f.write(i + "\n")


def check_connect_to_AP():
    while True:
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
            if ', '.join(addresses) != "No IP addr" and ', '.join(addresses) != "127.0.0.1":
                print('%s: %s' % (ifaceName, ', '.join(addresses)))
                return ', '.join(addresses)

def getmyIP():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    return local_ip


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
def reqKEY(Server_ADDR):
    while True:
        r = requests.get(Server_ADDR+"/getkey")
        if r.status_code == requests.codes.ok:
            print(r.text)
            key_now=r.text.split()[0][4:]
            date_now = datetime.now().date().strftime("%Y-%m-%d")
            saveKEY(date_now, key_now)
            break

def sendKEY(Server_ADDR):
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

def checkID(Server_ADDR):
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

def gentestKEY():
    global KEYS
    with open(KEY_FILE_PATH, 'rb') as handler:
        KEYS = pickle.load(handler)
        
    date_now = datetime.now().date().strftime("%Y-%m-%d")
    if not date_now in KEYS:
        KEYS[date_now] = secrets.token_bytes(8).hex()
    with open(KEY_FILE_PATH, 'wb') as handler:
        pickle.dump(KEYS, handler)

def getKEYtoday():
    global KEYS

    ''' File Path '''
    KEY_FILE_PATH="./KEY_FILE"
    
    
    with open(KEY_FILE_PATH, 'rb') as handler:
        KEYS = pickle.load(handler)
        
    date_now = datetime.now().date().strftime("%Y-%m-%d")
    if date_now in KEYS:
        return KEYS[date_now]
    else :
        print("I have no key today.")
        return ""


''' communicate with AP server '''
def sendID(ID, IP):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)
    IPID = IP + " " +ID
    message = str.encode(IPID)
    server.sendto(message, ('<broadcast>', 37020))
    print("message sent!") # for Debug

def recvID(ID):
    global APIP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket. IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(("", 3000))
    # client.settimeout(10)
    data, addr = client.recvfrom(1024)
    data = data.decode("utf-8")
    if data[0:6] == "List: ":
        writedata(data[6:], ID)
    elif data[0:3] == "AP:":
        APIP = data[3:]
    elif data[0:5] == "Here?":
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.settimeout(0.2)
        message = str.encode("I'm here")
        server.sendto(message, (APIP, 37020))
    else:

        if data == ID:
            return
        writedata(data, ID)

''' communicate with DB '''
# def saveID():


if __name__ == '__main__':

    # reqKEY()
    # for key in KEYS:
    #     print("my ID is ", computeID(bytes.fromhex(KEYS[key]), key))
    # sendKEY()
    gentestKEY()
    key_today = getKEYtoday()
    myID = computeID(bytes.fromhex(key_today), datetime.now().strftime("%Y-%m-%d-%H"))
    myIP = check_connect_to_AP()
    time.sleep(1)
    # myID = "1234"
    sendID(myID, myIP)
    while True:
        recvID(myID)

    # print(checkID())
