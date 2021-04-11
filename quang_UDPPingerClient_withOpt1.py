from socket import *
from datetime import datetime
import quang_config as config

clientSocket = socket(AF_INET, SOCK_DGRAM)
serverAddressPort = (config.address, config.port)

mnTime = 100000000000000
mxTime = 0
loss = 0
totalTime = 0

for i in range(10):
    try:
        current = datetime.now().timestamp()
        msg = 'Ping ' + str(i + 1) + ' | ' + str(datetime.fromtimestamp(current))
        clientSocket.sendto(msg.encode(), serverAddressPort)
        clientSocket.settimeout(1)
        data, addr = clientSocket.recvfrom(1024)
        RTT = datetime.now().timestamp() - current
        print ('RTT: {}'.format(RTT))
        totalTime += RTT
        mxTime = max(mxTime, RTT)
        mnTime = min(mnTime, RTT)
        print ('Response msg: {}'.format(data.decode()))
    except timeout:
        print ('{} Request timed out'.format('Ping ' + str(i + 1)))
        loss += 1

    print('**************************************************')

print('\n\n--- server ping statistics ----')
print('{} packets transmitted, {} received, {}% packet loss'.format(10, 10 - loss, loss * 10))
print('rtt min/avg/max = {}/{}/{}'.format(round(mnTime, 10), round(totalTime/(10-loss), 10), round(mxTime, 10)))