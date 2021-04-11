HBPORT = 12000
CHECKWAIT = 5

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from threading import Lock, Thread, Event
from time import time, ctime, sleep
import sys

class BeatDict:

    def __init__(self):
        self.dictLock = Lock( )
        self.sequence_number = 0
        self.old_time_recv = 0

    def get_sequence_number(self):
        self.dictLock.acquire( )
        ans=self.sequence_number
        self.dictLock.release( )
        return ans

    def update_sequence_number(self,x):
        self.dictLock.acquire( )
        self.sequence_number=x
        self.dictLock.release( )
    
    def update_old_time_recv(self,x):
        self.dictLock.acquire( )
        self.old_time_recv=x
        self.dictLock.release( )

    def extractSilent(self, howPast):

        self.dictLock.acquire( )
        if self.old_time_recv < time( ) - howPast:
            print("Client disconnect")
            self.sequence_number=0
        self.dictLock.release( )


class BeatRec(Thread):

    def __init__(self,DictFunc, port):
        Thread.__init__(self)
        self.DictFunc = DictFunc
        self.port = port
        self.recSocket = socket(AF_INET, SOCK_DGRAM)
        self.recSocket.bind(('', port))

    def run(self):

        while True:
            message, address = self.recSocket.recvfrom(1024)
            self.recSocket.sendto(message,address)
            message=message.decode()
            array=message.split()
            recv_seq=int(array[1])
            recv_time=float(array[2])

            if recv_seq==1:
                print("CLient connect")

            for i in range(self.DictFunc.get_sequence_number()+1,recv_seq):
                print("Dropped Packet: ",i)
            print("Received: ",message)

            self.DictFunc.update_sequence_number(recv_seq)
            self.DictFunc.update_old_time_recv(recv_time)

def main( ):
    global HBPORT, CHECKWAIT
    beatDictObject = BeatDict( )
    beatRecThread = BeatRec(beatDictObject, HBPORT)
    beatRecThread.start( )
    while True:
        beatDictObject.extractSilent(CHECKWAIT)
        sleep(CHECKWAIT)
if __name__ == '__main__':
    main(  )