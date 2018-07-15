import socket
import sys
from _thread import *
import string
from server_controler import ServerControler


class ServerSocket():
    HOST = '127.0.0.1'   
    PORT = 5555
    
    ENDSTR = "[||]"
    ERROR = "!**!"
    DEL = "[*]"
    AUTH = "[^^]"
    DEN = "[xx]"
	
    
    def readData(self,conn):
        data = ""
        
        try:
                       
            while not data.endswith(self.ENDSTR):
                
                data += conn.recv(1024).decode('utf8')  
            
            data = str(data).replace(self.ENDSTR,"")
            
            conn.sendall(self.ENDSTR.encode('utf8'))
            
        except Exception as e:
            print(e)
            raise IOError('Error connecting with remote address')
        
        return data  
        																												
    def connthread(self,conn):
    
    
        info_array = []
        
        try:
            for i in range(3): # read contract's address, contract's abi and authentication hashes
                info_array.append(self.readData(conn))
            
            ctr = ServerControler(info_array[0],info_array[1],info_array[2])
            r = ctr.authenticate()
            
            if r == 0:
                conn.sendall((self.AUTH + self.ENDSTR).encode('utf8'))                                       
            else:
                conn.sendall((self.DEN + self.ENDSTR).encode('utf8'))                                       
                
            
        except IOError:
            conn.sendall((self.ERROR + self.ENDSTR).encode('utf8'))                       
        finally:
            conn.close()
    
        
    def loop(self):
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
        
        try:
            s.bind((self.HOST,self.PORT))
        except Exception as e:
            print('Bind failed.')
            print(e)
            sys.exit()
        
        print('Socket bind complete')
        
        s.listen(10)
        
        print('Socket now listening')
         
        while 1:
            
            conn, addr = s.accept()
            start_new_thread(self.connthread ,(conn,))
            
        
        
        s.close()

if __name__ == "__main__":
    
    s = ServerSocket()
    s.loop()
