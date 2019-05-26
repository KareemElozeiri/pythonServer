import socket
import pickle

class Client():
    def __init__(self,target_ip,target_port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.target = (target_ip,target_port)
        self.sock.connect(self.target)
        self.header = 10

    def send_data(self,data):
        #turning the data into bytes
        data = pickle.dumps(data)
        #getting the size of data and putting them into the header of data
        data_len = bytes(f"{len(data):<{self.header}}","utf-8")
        data_package = data_len + data
        #sending the data to the server
        self.sock.send(data_package)

    def recv_data(self):
        data = b''
        data_len = int(self.sock.recv(self.header).strip())

        if data_len <= self.header:
            data += self.sock.recv(data_len)
        else:
            if data_len%self.header == 0:
                num_of_packets = int(data_len/10)
                #receiving the packets
                for i in range(num_of_packets):
                    data += self.sock.recv(self.header)
            else:
                last_packet_len = data_len%10
                num_of_packets = int((data_len-last_packet_len)/10)
                #receiving the packets whose length = 10
                for i in range(num_of_packets):
                    data += self.sock.recv(self.header)
                #receiving last packet
                data += self.sock.recv(last_packet_len)
        #returning the data back to its original form
        data = pickle.loads(data)
        return data         
