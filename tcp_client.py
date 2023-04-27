"""
Server receiver buffer is char[256]
If correct, the server will send a message back to you saying "I got your message"
Write your socket client code here in python
Establish a socket connection -> send a short message -> get a message back -> terminate
use python "input->" function, enter a line of a few letters, such as "abcd"
"""
import socket
HOST = '172.20.10.7'
PORT =  2000
def main():
    # TODO: Create a socket and connect it to the server at the designated IP and port
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
    # TODO: Get user input and send it to the server using your TCP socket
        inp = input("Input Message ")
        arr = bytes(inp, 'utf-8')
        s.sendall(arr)
    # TODO: Receive a response from the server and close the TCP connection
        data = s.recv(1024)
        print(f"{data!r}")
    pass


if __name__ == '__main__':
    main()
