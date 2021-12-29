from socket import *

def main():
    # Cria o host e a porta
    server_host = 'localhost'
    server_port = 5005
    
    # Cria o socket
    server = socket(AF_INET, SOCK_DGRAM)
    
    # Indica que o servidor foi iniciado
    print("Servidor iniciado!")
    
    # Bloco infinito do servidor
    while True:
        # Recebe a data e o endereço da conexão
        data, address = server.recvfrom(1024)
        
        # Imprime as informações da conexão
        print("Mensagem recebida de", str(address))
        print("Recebemos do cliente:", str(data))
        
        # Vamos mandar de volta a mensagem em eco
        answer = 'Resposta eco => ' + str(data)
        server.sendto(data, address)
        
    # Fechamos o servidor
    server.close()
    
if __name__ == '__main__':
    main()