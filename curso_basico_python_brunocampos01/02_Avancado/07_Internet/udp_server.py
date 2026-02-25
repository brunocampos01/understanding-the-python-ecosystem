from socket import socket, AF_INET, SOCK_DGRAM


def main():
    server_host = 'localhost'
    server_port = 5005

    server = socket(AF_INET, SOCK_DGRAM)
    server.bind((server_host, server_port))

    print("Server started!")

    try:
        while True:
            data, address = server.recvfrom(1024)

            print("Message received from", str(address))
            print("Received from client:", str(data))

            answer = 'Echo response => ' + str(data)
            server.sendto(data, address)
    finally:
        server.close()


if __name__ == '__main__':
    main()
