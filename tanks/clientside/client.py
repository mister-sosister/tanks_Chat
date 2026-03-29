from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet
import socket
import threading
import queue
import json
import os


PORT = None
IPADRESS = None

# этапы пользователя при подключении: нет подключенияя - подключился - обмен публичными ключами - обмен симметричными ключами - отправка логина - авторизован
NOCONNECTION = "NOCONNECTION"
CONNECTED = "CONNECTED"
PUBKEYEXC = "PUBKEYEXC"
SYMKEYEXC = "SYMKEYEXC"
SENDINGLOGIN = "SENDINGLOGIN"
AUTHORISED = "AUTHORISED"

stage = NOCONNECTION

server_public_key = None
sym_key = None
sym_str_key = None

priv_key = rsa.generate_private_key(65537, 4096)
pub_key = priv_key.public_key()

def changingStages(newcon):
    global stage
    oldstage = stage
    stage = newcon
    print(f"состояние было изменено с {oldstage} на {stage}")

def configRead():
    global PORT, IPADRESS
    CONFIGFILE = os.path.join(os.path.dirname(__file__), "client_config.json")

    
    a = open(CONFIGFILE, "r")
    b = json.load(a)
    PORT = b["client"]["port"]
    IPADRESS = b["client"]["ip"]
    print(PORT)
    print(IPADRESS)
dataq = queue.Queue()
servsocket = None




def byteStrToPack(bytestring):
    sendstring = int.to_bytes(len(bytestring), 4, "big") + bytestring
    
    return sendstring

def messaging_server( senddict: dict):
    global stage, server_public_key
    #3 проверка на шифровку симметричным ключом
    if stage == SYMKEYEXC or stage == AUTHORISED:
        print("зашифровка симметричным ключом")
        tosenddict = json.dumps(senddict)
        btosenddict = tosenddict.encode()
        endict = sym_key.encrypt(btosenddict)
        servsocket.send(byteStrToPack(endict))
        
    elif stage == PUBKEYEXC:
        print("зашифровка публичным ключом")
        tosenddict = json.dumps(senddict)
        btosenddict = tosenddict.encode()
        endict = server_public_key.encrypt(btosenddict, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
        servsocket.send(byteStrToPack(endict))
        
    elif stage == CONNECTED:
        tosenddict = json.dumps(senddict)
        servsocket.send(byteStrToPack(tosenddict.encode()))
        
    print(f"оптравлено сообщение {tosenddict} типа {type(tosenddict)}")
def dataAnalys():
    global dataq, server_public_key, pub_key, sym_key, sym_str_key, loginCon
    while True:
        
        try:
            data = dataq.get(timeout=1)
            print(f"получено сообщение {data}")
        except queue.Empty:
            continue
        #if data["code"] == "100":
        #    loginCon = False
        if data["code"] == "103":
            print(data["message"])
        elif data["code"] == "104":
            changingStages(AUTHORISED)
        elif data["code"] == "202":
            print(data["message"])
        elif data["code"] == "301":
            bytekey = data["key"].encode()
            server_public_key = serialization.load_pem_public_key(bytekey)
            messaging_server({"code" : "302", "key" : pub_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()})
            changingStages(PUBKEYEXC)
        elif data["code"] == "303":
            #sym_key = (data["key"].encode(), padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
            sym_str_key = data["key"]
            sym_key = Fernet(sym_str_key)
            changingStages(SYMKEYEXC)
            print(f"симметричный ключ {sym_key}")
        elif data["code"] == "403":
            print(data["message"])


def dataTakeOut(bytenum, socket):
    retstr = b""
    while len(retstr) < bytenum:
        takendata = socket.recv(bytenum - len(retstr))
        retstr += takendata

    return retstr   

def returnOneMsg(socket):
    bytehead = dataTakeOut(4, socket)
    head = int.from_bytes(bytehead, "big")
    msg = dataTakeOut(head, socket)
    return msg


def dataTake():
    global dataq, servsocket
    while True:
        #try:
        server_data = returnOneMsg(servsocket)
        print(f"стадия дешифровки {stage}")
        if stage == PUBKEYEXC:
            server_data = priv_key.decrypt(server_data, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))

        elif stage == SYMKEYEXC or stage == AUTHORISED:
            server_data = sym_key.decrypt(server_data)

            
        decodedData = server_data.decode("UTF-8")
        if decodedData.strip() == "":
            print("пришла пустая строка")
        else:
             dataq.put(json.loads(decodedData.strip()))
        #except Exception as dataTakeException:
        #    print(f"Ошибка Datatake {dataTakeException}")




def commanding():
    global condition, NOLOGINCON
    while True:
        command = input()
        if command == "send":
            whoToSend = input("напишите логин пользователя: ")    
            whatToSend = input("сообщение: ")
            messaging_server({"code" : "201", "whom" : whoToSend, "what" : whatToSend})
        elif command == "send login":
            
            login = input("введите логин ")
            messaging_server({"code": "101", "login" : login})
        

def connectingts():
    
    global servsocket
    configRead()
    servsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servsocket.connect((IPADRESS, PORT))   
    rec_thread = threading.Thread(target=dataTake, daemon=True)
    analysis_trd = threading.Thread(target=dataAnalys, daemon=True)
    com_thread = threading.Thread(target=commanding, daemon=True)
    changingStages(CONNECTED)
    rec_thread.start()
    analysis_trd.start()
    com_thread.start()
    rec_thread.join()
    analysis_trd.join()
    com_thread.join()
    
    
connectingts()
