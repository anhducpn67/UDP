from socket import *
import quang_config as config

def parse(msg):
    id1 = msg.find('Packet: ')
    id1 += len('Packet: ')
    packetOrder = 0
    while True:
        if msg[id1].isdigit():
            packetOrder = packetOrder * 10 + int(msg[id1])
            id1 += 1
        else:
            break   

    id1 = msg.find('Timestamp: ')
    id1 += len('Timestamp: ')
    sendingTime = 0
    while True:
        if (msg[id1].isdigit()):
            sendingTime = sendingTime * 10 + int(msg[id1])
            id1 += 1
        else:
            break
    return (packetOrder, sendingTime)

clientDelay = 3
deadTime = 12
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', config.port))
lastReceive = -1

while True:
    try:
        serverSocket.settimeout(deadTime)
        msg, addr = serverSocket.recvfrom(1024)
        (packetOrder, sendingTime) = parse(msg.decode())
        print ('Packet: {} | Timestamp: {}\n'.format(packetOrder, sendingTime))
        if lastReceive == -1:
            lastReceive = sendingTime
            print ('*************************************************\n')
            continue
        numberPacketLoss = int((sendingTime - lastReceive)//clientDelay - 1)
        for i in range(-numberPacketLoss, 0):
            print ('Packet {} loss'.format(packetOrder + i))
        lastReceive = sendingTime
    except timeout:
        print ('Client stopped!')
        break   
    print ('*************************************************\n')



