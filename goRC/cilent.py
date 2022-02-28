from socket import *
import ctypes
import sys


tcp_client = socket(AF_INET, SOCK_STREAM)
ip = ""
try:
    if sys.argv.index("--ip")+1 < len(sys.argv):
        ip = sys.argv[sys.argv.index("--ip")+1]
except:
    pass
port = 2550


def cilent_forever():
    while True:
        send("cd")
        pwd = tcp_client.recv(2048).decode("utf-8").replace("\r\n", "")
        title = "goRC [{}] : {}".format(ip, pwd)
        ctypes.windll.kernel32.SetConsoleTitleW(title)
        prompt = "{} {}>".format("goRC", pwd)
        msg = input(prompt).strip()
        if not msg:
            continue
        if msg == "exit":
            tcp_client.close()
            break
        send(msg)
        data = tcp_client.recv(20480)
        print(data.decode("utf-8"))


def send(cmdstr):
    tcp_client.sendall("{}{}".format(cmdstr, "EOF").encode("utf-8"))


if __name__ == "__main__":
    if not ip:
        ip = str(input("ip:"))
    ip_port = (ip, port)
    tcp_client.connect(ip_port)
    cilent_forever()
    tcp_client.close()
