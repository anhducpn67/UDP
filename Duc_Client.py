import time
from socket import *
import Duc_project_config as config

# Parameters
serverName = config.serverName
serverPort = config.serverPort
clientSocket = socket(AF_INET, SOCK_DGRAM)
Time = time.time()
numberPacketsLoss = 0
Minimum = 99999999
Maximum = 0
TotalTime = 0

# Sent packets
for i in range(1, config.numberPacketsSent + 1):
    try:
        clientSocket.settimeout(config.timeOutForClient)
        start = time.time() - Time
        message = "Ping " + str(i) + " " + str(round(start * 1000, 3)) + " ms"
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        rtt = round((time.time() - Time - start) * 1000, 3)
        Minimum = min(rtt, Minimum)
        Maximum = max(rtt, Maximum)
        TotalTime = TotalTime + rtt
        modifiedMessage = modifiedMessage.decode()
        modifiedMessage = modifiedMessage + " " * (30 - len(modifiedMessage))
        print(modifiedMessage + "time =", rtt, "ms")
    except OSError:
        print("Request timed out")
        numberPacketsLoss += 1

clientSocket.close()
# Statistics for packets
print("--- " + config.serverName + " ping statistics ---")
print("\t" + "Send =", config.numberPacketsSent, end=", ")
print("Received =", config.numberPacketsSent - numberPacketsLoss, end=", ")
print("Lost =", numberPacketsLoss, end=" ")
print("(", round((numberPacketsLoss / config.numberPacketsSent) * 100, 1), "% lost)", sep="")

# Statistics for RTT
print("Approximate round trip times in milli-seconds:")
print("\t" + "Minimum =", Minimum, "ms", end=", ")
print("Maximum =", Maximum, "ms", end=", ")
print("Average =", round(TotalTime / (config.numberPacketsSent - numberPacketsLoss), 3), "ms")
