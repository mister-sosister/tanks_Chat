import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet
import socket
import servside_client
import queue
import json
import os
import lobby

sym_key = Fernet.generate_key()
key_obj = Fernet(sym_key)

lobbies = []
#priv_key = rsa.generate_private_key(65537, 4096)
#pub_key = priv_key.public_key()
PORT = None
IPADRESS = None
clients : list[servside_client.ClientOnServer] = [] 

endevent = threading.Event()
#[+] — успех, положительное событие.
#[-] — ошибка или что-то пошло не так.
#[*] — информация общего характера (обычно «статус»).
#[!] — предупреждение (что-то потенциально опасное, но не критично).
#[?] — запрос/ожидание ввода пользователя.
#[>] — процесс/действие выполняется.
#[<] — получено что-то (например, ответ от сервера).

def configRead():
    global PORT, IPADRESS
    configfile = os.path.join(os.path.dirname(__file__), "serv_config.json")
    
    a = open(configfile, "r")
    b = json.load(a)
    PORT = b["server"]["port"]
    IPADRESS = b["server"]["ip"]
    print(IPADRESS)
    print(PORT)
    
   
    
    
def DataAnalys(client : servside_client.ClientOnServer):
    global endevent, lobbies
    while True:
        if endevent.is_set():
            print("Dataanalys over")
            return
        try:
            data = client.dataq.get(timeout=1)
            print(f"получено сообщение {data}")
        except queue.Empty:
            continue
        
        if data["code"] == "101":
            ...
        #    
        #    if getUserWithLogin(data["login"]) != None:
        #        messaging_client(client, {"code" : "103", "message" : (f"[<] login {data['login']} is already taken")})
        #        print(f"логин {data['login']} уже занят")
        #        messaging_client(client, {"code" : "100"})
        #    else:
        #        setting_client(client, data)
        #        messaging_client(client, {"code" : "104", "message" : f"login {data['login']} "})
        elif data["code"] == "201":
            messaging_client_sym(getUserWithLogin(data["whom"]), {"code" : "202", "message" : data["what"], "from" : client.login})
        elif data["code"] == "302":
            setting_client(client, data)
        elif data["code"] == "404":
            print(f"пользователь {client.login} отключился")
            return
        elif data["code"] == "501":
            if getUserWithLogin(data["tologin"]) == None:
                messaging_client_sym(client, {"code": "502", "message" : "клиента с таким логином не существует"})
            else:
                messaging_client_sym(getUserWithLogin(data["tologin"]), {'code' : "503", "message" : f"вам пришло приглашение в группу от пользователя {data['fromlogin']}", "fromlogin" : data["fromlogin"]})
        elif data["code"] == "504":
            a = lobby.game_lobby(data["flogin"], data["slogin"])
            a.check_status()
            lobbies.append(a)
            messaging_client_sym(getUserWithLogin(data["slogin"]), {"code" : "505"})
        elif data["code"] == "506":
            messaging_client_sym(getUserWithLogin(data["slogin"]), {"code" : "507"})
def dataTakeOut(bytenum, socket):
    retstr = b""
    while len(retstr) < bytenum:
        try:
            takendata = socket.recv(bytenum - len(retstr))
            retstr += takendata
        except TimeoutError:
            continue
    return retstr

def returnOneMsg(socket):
    bytehead = dataTakeOut(4, socket)
    head = int.from_bytes(bytehead, "big")
    msg = dataTakeOut(head, socket)
    return msg


def DataTake(client : servside_client.ClientOnServer):
    global clients
    while True:
        try:
            server_data = returnOneMsg(client.socket)
            print(server_data)
        except ConnectionResetError:
            client.dataq.put({"code" : "404"})
            clients.remove(client)
            break
        except TimeoutError:
            if endevent.is_set():
                print("datatake over")
                return
            else:
                continue
        
        #print(f"пришло сообщение {server_data}")
        #if client.gotSymKey == True:
        decodedData = key_obj.decrypt(server_data)
        #elif client.key != None:
        #    decodedData = key_obj.decrypt(server_data, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
        #else:
        #    decodedData = server_data
        a = json.loads(decodedData.decode())

        client.dataq.put(a)


def byteStrToPack(bytestring):
    sendstring = int.to_bytes(len(bytestring), 4, "big") + bytestring
    return sendstring

def messaging_client_none(client: servside_client.ClientOnServer, senddict: dict):
    
    tosenddict = json.dumps(senddict)
    client.socket.send(byteStrToPack(tosenddict.encode()))
    print(f"оптравлено сообщение {tosenddict} типа {type(tosenddict)}")
    
    
def messaging_client_sym(client: servside_client.ClientOnServer, senddict: dict):
    tosenddict = json.dumps(senddict)    
    sbtsdict = tosenddict.encode()
    client.socket.send(byteStrToPack(key_obj.encrypt(sbtsdict)))
    print(f"оптравлено сообщение {tosenddict} типа {type(tosenddict)}")
    
def messaging_client_pub(client: servside_client.ClientOnServer, senddict: dict, key):
    senddict["key"] = senddict["key"].decode()
    tosenddict = json.dumps(senddict)
    sbtsdict = tosenddict.encode()
    client.socket.send(byteStrToPack(key.encrypt(sbtsdict, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))))
    print(f"оптравлено сообщение {tosenddict} типа {type(tosenddict)}")
    
def setting_client(client: servside_client.ClientOnServer, whattoset):
    if whattoset["code"] == "101":
        client.login = whattoset["login"]
    #    messaging_client_sym(client, {"code" : "103", "message" : (f"[<] логин {whattoset['login']} задан")})
    #    messaging_client_sym(client, {"code" : "403", "message" : "данные клиента были изменены"})
    #    print(client.login)
        
    if whattoset["code"] == "302":
        client.key = serialization.load_pem_public_key(whattoset["key"].encode())
        messaging_client_sym(client, {"code" : "303", "key" : sym_key.decode()})
        print("отправлен симметричный ключ")
        client.gotSymKey = True
        #messaging_client(client, {"code" : "100"})
    
def commanding():
    while True:
        command = input()
        if command == "endserver":
            endevent.set()
            print("сервер эакрывается")
            return
    
    
def getUserWithLogin(login : str):
    global clients
    for i in range(len(clients)):
        print(clients[i].login)
        if clients[i].login == login:
            return clients[i]
    return None
#байты - расшифровка байтов - превращение в текст - превращение в словарь

def auth_user(usocket):
    
    #пользователь отправляет публичный ключ - сервер шифрует симметричный ключ и отправляет его - клиент отправляет логин
    print(f"[+] клиент {usocket} был подключен")
    a = servside_client.ClientOnServer(usocket)
    pubkey = json.loads(returnOneMsg(usocket))["key"]
    print("1")
    obj_pubkey = serialization.load_pem_public_key(pubkey.encode())
    print("2")
    messaging_client_pub(a, {"code" : "303", "key" : sym_key}, obj_pubkey)
    print("3")
    login = json.loads(key_obj.decrypt(returnOneMsg(usocket)))
    print("4")
    setting_client(a, login)
    print("4")
    messaging_client_sym(a, {"code" : "103", "message" : (f"[<] логин {login['login']} задан")})
    #messaging_client(a, {"code" : "104", "message" : f"login {data['login']} "})
    clients.append(a)
    a.startTakeIn(DataTake)
    a.startanAlysis(DataAnalys)
    print(f"пользователь {a} был авторизован")
    usocket.settimeout(1)
    
def accepting_connections():
    global pub_key, endevent
    newsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    newsocket.bind((IPADRESS, PORT))
    newsocket.listen()
    
    while True:

        socket_data = newsocket.accept()
        socket_data[0].settimeout(1)

        #добавить таймаут к сокетдате
        threading.Thread(target=auth_user, daemon= True, args=(socket_data[0], )).start()

        
def launchServ():
    configRead()
    print("[>] сервер запускается")
    commtrd = threading.Thread(target=commanding, daemon=True)
    commtrd.start()
    accepting_connections()


    
launchServ()


