import random
import time
from socket import *
import Duc_project_config as config

# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', config.serverPort))
while True:
    print('Ready to serve...')
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    print("Connected to address:", address)
    # Capitalize the message from the client
    message = message.upper()
    # If rand is less is than percentage loss, we consider the packet lost and do not respond
    if rand < config.percentageLoss:
        continue
    # Otherwise, the server responds
    serverSocket.sendto(message, address)
