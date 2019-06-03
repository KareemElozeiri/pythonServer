import socket
import pickle

class Client():
    def __init__(self,target_ip,target_port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #this line is for the reusablility of the client addr in case of shutting down
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.target = (target_ip,target_port)
        self.sock.connect(self.target)
        self.headerSize = 10

    def send_data(self,data):
        #turning the data into bytes
        data = pickle.dumps(data)
        #getting the size of data and putting them into the header of data
        data_len = bytes(f"{len(data):<{self.headerSize}}","utf-8")
        data_package = data_len + data
        #sending the data to the server
        self.sock.send(data_package)

    def recv_data(self):
        data = b''
        data_len = int(self.sock.recv(self.headerSize).strip())

        if data_len <= self.headerSize:
            data += self.sock.recv(data_len)
        else:
            if data_len%self.headerSize == 0:
                num_of_packets = int(data_len/self.headerSize)
                #receiving the packets
                for i in range(num_of_packets):
                    data += self.sock.recv(self.headerSize)
            else:
                last_packet_len = data_len%self.headerSize
                num_of_packets = int((data_len-last_packet_len)/self.headerSize)
                #receiving the packets whose length = 10(headerSize)
                for i in range(num_of_packets):
                    data += self.sock.recv(self.headerSize)
                #receiving last packet
                data += self.sock.recv(last_packet_len)
        #returning the data back to its original form
        data = pickle.loads(data)
        return data
