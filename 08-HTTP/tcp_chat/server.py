import socket
import argparse
import threading


LIST_OF_CLIENTS = []


def remove(connection):
    global LIST_OF_CLIENTS
    if connection in LIST_OF_CLIENTS:
        LIST_OF_CLIENTS.remove(connection)


def broadcast(message, connection):
    global LIST_OF_CLIENTS
    for clients in LIST_OF_CLIENTS:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)


def client_treading(conn, addr):
    conn.send(b"Welcome to this chat")

    while True:
        try:
            message = conn.recv(2048)
            if message:
                print(b"<" + addr[0] + b">:" + message)
                message_to_send = b"<" + addr[0] + b">:" + message
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue


def main(IP_address, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP_address, port))
    server.listen(10)

    while True:
        conn, addr = server.accept()
        global LIST_OF_CLIENTS
        LIST_OF_CLIENTS.append(conn)
        print(addr[0], b"connected")
        threading.Thread(target=client_treading, args=(conn, addr)).start()


    conn.close()
    server.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--IP', default='0.0.0.0')
    parser.add_argument('--Port', default='10000')
    args = parser.parse_args()

    try:
        IP_addr = str(args.IP)
        Port_num = int(args.Port)
    except ValueError:
        raise SystemExit("correct usage: script_name, --IP IP_adress, --Port port_number")

    main(IP_addr, Port_num)
