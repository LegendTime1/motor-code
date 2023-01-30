import socket

def motor(m:int, n:int):
    serverAddressPort   = ("192.168.1.102", 8002) #input the server address and port
    bufferSize          =  1024
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Send to server using created UDP socket

   
    if m >= 100 :
        x = "0"+ str(m)
    elif m >= 10:
        x = "00" + str(m)
    elif m >= 0:
        x = "000" + str(m)
    elif m >-10:
        x = "-00" + str(-1*m)
    elif m >= -100:
        x = "-0" + str(-1*m)
    else:
        x = str(m)
    if n >= 100 :
        y = "0"+ str(n)
    elif n >= 10:
        y = "00" + str(n)
    elif n >= 0:
        y = "000" + str(n)
    elif n >-10:
        y = "-00" + str(-1*n)
    elif n >= -100:
        y = "-0" + str(-1*n)
    else:
        y = str(n)
    bytesToSend = str.encode(x+y+"\n")
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    #print(x+"p"+y)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Client:{}".format(msgFromServer[0].decode())
    #print(msg)