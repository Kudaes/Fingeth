import socket
import sys
import string


class FingerSocket():
    HOST = '127.0.0.1'   
    PORT = 6666

    ENDSTR = "[||]"
    ERROR = "!**!"
    DEL = "[*]"
              
              
    def __readData(self,conn):
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

    def __connRead(self,conn):

        finger = ""

        try:
            
            finger = self.__readData(conn)            

        except IOError:
            conn.sendall((self.ERROR + self.ENDSTR).encode('utf8'))
            raise IOError('Socket error at reading data.')
        finally:
            conn.close()
        
        return finger

    def receiveFingerprint(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((self.HOST,self.PORT))
        except Exception as e:
            raise IOError('Bind failed.')

        s.listen(5)

        print('Socket now listening...')

       

        conn, addr = s.accept()
        f = self.__connRead(conn)
        s.close()
        
        return f.split(self.DEL)


    def sendFingerprint(self,finger,ip):
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip,self.PORT))   
        
        chain = finger[0]
        for i in range(len(finger)-1):
            chain += self.DEL + finger[i+1]
        chain += self.ENDSTR
        
        try:
            s.sendall(chain.encode('utf8'))
            data = ""
            
            while not data.endswith(self.ENDSTR):
                data += s.recv(1040).decode('utf8')
                
            data = str(data).replace(self.ENDSTR,"")
            if data == self.ERROR:
                raise IOError('Connection error.')            
        except:
            raise IOError('Connection error.')
        finally:
            s.close()