import json
import random
import socket
import time
from datetime import datetime
from ws_chat_sensor import get_sensor_data

while True:
    s = socket.socket()
    host = "10.167.217.78"
    port = 12345

    try:
        s.connect((host, port))
        yanit = s.recv(1024)
        print("Server:", yanit.decode("utf-8"))

        data = get_sensor_data() 

        json_data = json.dumps(data)
        s.send(json_data.encode("utf-8"))


        s.close()
    except socket.error as msg:
        print("[Server aktif değil.] Mesaj:", msg)

    time.sleep(1)
