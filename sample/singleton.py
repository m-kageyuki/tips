class Singleton:
    __instance = None

    @staticmethod 
    def getInstance():
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        if Singleton.__instance != None:
            raise Exception("this is singleton.")
        else:
            self.__conn = None
            self.__is_connected = False
            Singleton.__instance = self
         
    def connect(self, val):
        if self.__is_connected:
            return
        self.__conn = val
        self.__is_connected = True
        check()
    
    def is_connect(self):
        return self.__is_connected
    
    def getConn(self):
        return self.__conn
    
    def disconnect(self):
        self.__conn = None
        self.__is_connected = False

def check():
    print("this is test.")

    

