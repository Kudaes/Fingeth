import socket

class ClientSocket():        
    

    ENDSTR = "[||]"
    ERROR = "!**!"
    DEL = "[*]"
    AUTH = "[^^]"
    
    
    def __init__(self,address="",abi="",hashes=None):
        self.address = address
        self.abi = abi
        self.hashes = hashes
        
        
    def authenticate(self):
        

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        host = input("Remote IP address: ")
        port = int(input("Remote port: "))
        
        s.connect((host,port))
        dataToSend = []
        dataToSend.append(str(self.address) + self.ENDSTR)
        dataToSend.append(self.abi + self.ENDSTR)
        
        chain = self.hashes[0].hex()
        for i in range(len(self.hashes)-1):
            chain += self.DEL + self.hashes[i+1].hex()
        
        chain += self.ENDSTR
        dataToSend.append(chain)
        try:
            for i in dataToSend:
                
                s.sendall(i.encode('utf8'))
                data = ""
                
                while not data.endswith(self.ENDSTR):
                    data += s.recv(1040).decode('utf8')
                    
                data = str(data).replace(self.ENDSTR,"")
                if data == self.ERROR:
                    raise IOError('Connection error.')
                
            data = ""  
            while not data.endswith(self.ENDSTR):
                data += s.recv(1040).decode('utf8') 
                
        except:
            raise IOError('Connection error.')
        finally:
            s.close()  
            
        data = str(data).replace(self.ENDSTR,"")
        
        if data == self.AUTH:
            return 0
        elif data == self.ERROR:
            return -1
        else:
            return 1

        
    
