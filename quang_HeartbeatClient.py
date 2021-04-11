from socket import *
import quang_config as config
import time
import random

delayTime = 3
clientSocket = socket(AF_INET, SOCK_DGRAM)
serverAddressPort = (config.address, config.port)
orderPacket = 0

while True:
    rand = random.randint(0, 5)
    orderPacket += 1
    if ((rand > 1) or (orderPacket == 1)):
        clientSocket.sendto(('Packet: {} | Timestamp: {} '.format(orderPacket, round(time.time(), 0))).encode(), serverAddressPort)
    time.sleep(delayTime)