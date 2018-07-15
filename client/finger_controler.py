from time import gmtime, strftime
from pathlib import Path
from finger_socket import FingerSocket

class FingerprintControler():
    
    pathFinger = "./fingerprints/"
    
    def exportFingerprint(self,finger):
        
        time = strftime("%Y%m%d%H%M%S", gmtime())
        my_file = Path(self.pathFinger + time + '.txt')
        
        try:
            with open(my_file,'w') as f:
                for fin in finger:
                    f.write(fin + '\n')
        except IOError:
            return -1,None
        
        return 0,str(self.pathFinger + time + '.txt')
    
    def readFingeprint(self,path):
        
        my_file = Path(path)
        finger = []
        
        try:
            with open(my_file,'r') as f:
                finger.append(f.readline().replace('\n',''))
        except IOError as e:
            return None
        
        return finger   
            
        
    def sendFingerprint(self,finger,ip):
        
        fs = FingerSocket()
        try:
            fs.sendFingerprint(finger,ip)
        except IOError:
            return -1
        
        return 0
    
    def receiveFingerprint(self):
        
        fs = FingerSocket()
        finger = None
        try:
            finger = fs.receiveFingerprint()
        except IOError:
            return None
        
        
        return finger