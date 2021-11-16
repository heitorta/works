import sys
import socket
def main():
    try:
        objeto_conexao = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        print('Socket criado com sucesso. ')
        host = 'localhost'
        porta = 5433
        mensagem = 'Hello World '
    except socket.error as erro:
        print('Houve um erro. ')
        print(erro)
        sys.exit()
    try:
        print(f'Cliente: {mensagem}')
        objeto_conexao.sendto(mensagem.encode(),(host,5432))
        dados = objeto_conexao.recvfrom(4096)
        dados = dados.decode()
        print(f'Cliente: {dados}')
    finally:
        print('Cliente fechando a conexão')
        objeto_conexao.close()
if __name__ == '__main__':
    main()



