import socket
import serial
import time

localIP     = "192.168.254.96"
localPort   = 8003
bufferSize  = 1024     
address = ("192.168.254.107",8003)

# Create a datagram socket

def server():
    
    #message = []
    arduino1 = serial.Serial(port='/dev/ttyUSB0',baudrate=115200)
    #arduino2 = serial.Serial(port='/dev/ttyUSB1',baudrate=115200)

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")
    
    # Listen for incoming datagrams
    while(True):
        print(1)
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0].decode()
        clientMsg = "Message from Client:{}".format(message)
        print(clientMsg)
        arduino1.write(bytesAddressPair[0])
        #arduino2.write(bytesAddressPair[0])
        value = arduino1.readline()
        #print(value)
        #print(type(value))
        #feedback = str.encode(value)
        UDPServerSocket.sendto(value,bytesAddressPair[1])
        time.sleep(0.002)

server()
