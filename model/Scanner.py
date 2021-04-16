import socket
import sys
from queue import Queue
import threading 

ascci_banner = """
 _____         _      _____                         
|  _  |___ ___| |_   |   __|___ ___ ___ ___ ___ ___ 
|   __| . |  _|  _|  |__   |  _| .'|   |   | -_|  _|
|__|  |___|_| |_|    |_____|___|__,|_|_|_|_|___|_|  
                                                    
"""

class Scanner:
    def __init__(self, threads, host, portMax=65000):
        self.hostServer = host
        self.threads = threads
        self.lenght = 70
        self.portMax = portMax
        self.timeout = 0.01
        self.queue = Queue()

    def displayDescription(self):
        print(ascci_banner)
        print("-" * self.lenght)
        print("Host adress: " + self.hostServer)
        print("Scan from port 1 to port "+str(self.portMax))
        print("-" * self.lenght+'\n')

    def scanPort(self,port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.hostServer, port))
            if result == 0:
                print('Target '+self.hostServer+' Port '+str(port)+' open')
            sock.close()
        except socket.gaierror:
            pass
        except socket.error:
            print("The server does not answer")
            sys.exit()

    def threader(self):
        while True:
            worker = self.queue.get()
            self.scanPort(worker)
            self.queue.task_done()
        
    def scanner(self):
        try:
            for x in range(30):
                t = threading.Thread(target=self.threader)
                t.daemon = True
                t.start()
        
            for worker in range(1,self.portMax):
                self.queue.put(worker)
            return self.queue.join()
        except KeyboardInterrupt:
            print('\nClose Program ...')
            sys.exit()
