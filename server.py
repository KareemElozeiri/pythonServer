import socket
import pickle

class Server():
    def __init__(self,port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #list to store clients(sockets and addresses)
        self.connections = []
        self.headerSize = 10
        self.addr = (socket.gethostname(),port)
        self.sock.bind(self.addr)
        print(f"Server is now running at {self.addr[0]}:{self.addr[1]}...")
        self.sock.listen(5)
        print("Server is waiting for clients to connect...")

    #this method is responsable for accepting the connections from clients and putting them in a list
    def accept_conn(self):
        client_socket , client_addr = self.sock.accept()
        client = {"Socket":client_socket,"address":client_addr}
        self.connections.append(client)
        print(f"Server accepted connection from {client_addr[0]}:{client_addr[1]}...")

    def send_data(self,client_num,data):
        #turning the data into bytes
        data = pickle.dumps(data)
        #getting the size of the data and putting it in the header of data
        data_len = bytes(f"{len(data):<{self.headerSize}}","utf-8")
        data_package = data_len + data
        client_sock = self.connections[client_num]["Socket"]
        #sending the data to the client
        client_sock.send(data_package)

    def recv_data(self,client_num):
        data = b''
        client_sock = self.connections[client_num]["Socket"]
        data_size = int(client_sock.recv(self.headerSize).strip())

        if data_size <= self.headerSize:
            data += client_sock.recv(data_size)
        else:
            if data_size%self.headerSize == 0:
                num_of_packets = int(data_size/self.headerSize)
                #receiving the packets
                for i in range(num_of_packets):
                    data += client_sock.recv(self.headerSize)
            else:
                #getting the size of last packet which is less than 10
                last_packet_len = data_size%self.headerSize
                #getting the number of packets whose size is equal to 10
                num_of_packets = int((data_size - last_packet_len)/self.headerSize)
                #receiving packets whose size=10
                for i in range(num_of_packets):
                    data += client_sock.recv(self.headerSize)
                #receiving the remaining packet
                data += client_sock.recv(last_packet_len)
        #returning the data back to its original form
        data = pickle.loads(data)
        return data
