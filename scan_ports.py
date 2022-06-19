import socket
import threading
import time
import ipaddress
import requests


def host_port_scan(host, port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        if s.connect_ex((host, port)) == 0:
            list_open_port.append([port, host])
            s.close()
    except:
        pass


def check_server(list_open_p):

    for port, host in list_open_p:
        message_server = ''
        if port == 80 or port == 443:
            time.sleep(0.1)
            try:
                response = requests.head(f'http://{host}', timeout=1)
                if response.headers["Server"]:
                    message_server = f'-- Server: {response.headers["Server"]}'
            except:
                pass

        print(f'{host} {port} OPEN {message_server}')


def main():
    for ip in ipaddress.IPv4Network(ip_range):
        host = str(ip)
        for port in list_ports:
            if port == 80 or port == 443:
                time.sleep(0.1)
            th = threading.Thread(target=host_port_scan, kwargs={"host": host, "port": port}, daemon=True)
            th.start()


if __name__ == "__main__":
    list_open_port = []

    ip_range = input('Enter IP range (example "192.168.1.0/24"): ')
    list_ports = list(map(int, input('Enter ports (example "80, 22, 443"): ').split(",")))

    main()
    check_server(list_open_port)

