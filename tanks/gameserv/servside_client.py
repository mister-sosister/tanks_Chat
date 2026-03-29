from queue import Queue
import threading
class ClientOnServer:
    def __init__(self, socket):
        self.socket = socket
        self.login = None
        self.dataq = Queue()
        self.threadin = None
        self.threadanalysis = None
        self.key = None
        self.gotSymKey = False

    def startanAlysis(self, func):
        self.threadanalysis = threading.Thread(target=func, daemon=True, args=(self,))
        self.threadanalysis.start()

    
    def startTakeIn(self, func):
        self.threadin = threading.Thread(target=func, daemon=True, args=(self,))
        self.threadin.start()
