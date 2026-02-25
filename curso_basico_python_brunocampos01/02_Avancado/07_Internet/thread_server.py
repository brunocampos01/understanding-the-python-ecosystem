from socketserver import BaseRequestHandler, ThreadingTCPServer
import time


def now():
    return time.ctime(time.time())


def configure_server():
    server_host = 'localhost'
    server_port = 5000
    return (server_host, server_port)


class HandlesClientRequests(BaseRequestHandler):

    def handle(self):
        print(self.client_address, now())

        time.sleep(5)

        while True:
            data = self.request.recv(1024)

            if not data:
                break

            answer = 'Echo response => {data} at {time}'.format(
                data=data, time=now()
            )

            self.request.send(answer.encode())

        self.request.close()


if __name__ == '__main__':
    ip_address = configure_server()
    server = ThreadingTCPServer(ip_address, HandlesClientRequests)
    server.serve_forever()
