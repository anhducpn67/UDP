import socket
import time
import random
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ('localhost', 12000)
sock.settimeout(1)

sequence_number = 0

while sequence_number<20:
    start = time.time()
    sequence_number+=1
    message = 'Ping ' + str(sequence_number) + ' ' + str(start)

    try:

        # mô phỏng timeout    
        if random.randint(0,10)<2:
            time.sleep(5);
            raise socket.timeout

        # mô phỏng mất gói tin
        if random.randint(0,10)<4:
            continue;
        sent = sock.sendto(message.encode(), server_addr)
        print("Sent: " + message)
        data, server = sock.recvfrom(1024)
        print("Received: " + data.decode())
    except socket.timeout:
        print("Requested Time out\n")
        sequence_number=0

print("closing socket")
sock.close()