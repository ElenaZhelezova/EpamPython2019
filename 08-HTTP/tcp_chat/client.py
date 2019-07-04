import sys
import select
import socket
import argparse


def main(IP_address, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP_address, port))

    while True:
        socket_list = [sys.stdin, client]
        read_sockets, write_socket, error_socket = select.select(socket_list, [], [])

        for socks in read_sockets:
            if socks == client:
                message = socks.recv(2048)
                print(message)
            else:
                message = sys.stdin.readline()
                client.send(message)
                sys.stdout.write(b"<You>: ")
                sys.stdout.write(message)
                sys.stdout.flush()

    client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--IP', default='localhost')
    parser.add_argument('--Port', default='10000')
    args = parser.parse_args()

    try:
        IP_addr = str(args.IP)
        Port_num = int(args.Port)
    except ValueError:
        raise SystemExit("correct usage: script_name, --IP IP_address, --Port port_number")

    main(IP_addr, Port_num)
