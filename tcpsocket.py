from os import terminal_size
import os
import socket
import sys
def main():
    try:
        objeto_conexão = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as erro:
        print('Houve um erro. A conexão falhou.')
        print(erro)
        sys.exit()
    print('Socket criado.')

    host = input('Insira o host ou IP:  ')
    porta_host = int(input('Insira a porta a se conectar:  '))
    try:
        objeto_conexão.connect((host, porta_host))
        print(f'Cliente TCP conectado com sucesso no host {host} e porta {porta_host}')
        objeto_conexão.shutdown(3)
    except socket.error as erro:
        print(f'A conexão com {host} pela porta {porta_host} não teve sucesso. ' )
        print(erro)
        sys.exit()
if __name__ == '__main__':
    main()


