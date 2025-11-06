# Importa os modulos
from socketserver import BaseRequestHandler, ThreadingTCPServer
import time


# Devolve a hora atual
def now():
    return time.ctime(time.time())


# Configura o servidor com o host e a porta
def configure_server():
    server_host = 'localhost'
    server_port = 5000
    return (server_host, server_port)


# Classe que lida com as requisições do cliente
class HandlesClientRequests(BaseRequestHandler):
    
    def handle(self):
        # Lida com cada requisição do cliente
        print(self.client_address, now())
        
        # Simula processamento dos dados
        time.sleep(5)
    
        while True:
            # Recebe dados enviados pelo cliente
            data = self.request.recv(1024)
        
            # Se não receber nada paramos o loop
            if not data: break
            
            # Escreve a resposta
            answer = 'Resposta eco => {data} as {time}'.format(data=data, time=now())
        
            # Servidor manda de volta a resposta
            self.request.send(answer.encode())
        
        # Fecha a conexão criada depois de responder o cliente
        self.request.close()

        
# Cria uma thread server e lida com a entrada e requisitos do cliente
ip_address = configure_server()
server = ThreadingTCPServer(ip_address, HandlesClientRequests)
server.serve_forever()