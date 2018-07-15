import subprocess
import platform as p
import string
#import uuid

class FingerPrinter():
    
    bios_cmd = ['dmidecode -s bios-vendor','dmidecode -s bios-version','dmidecode -s bios-release-date','dmidecode -s baseboard-manufacturer','dmidecode -s baseboard-product-name']
    
    def __sh(self,cmd, in_shell=False, get_str=True):
        output = subprocess.check_output(cmd, shell=in_shell)
        if get_str:
            return str(output, 'utf-8').replace('\n','')
        return output 
    
    def __getBiosInfo(self,num=len(bios_cmd)):
        
        info = []
        for i in range(num):
            cmd = self.bios_cmd[i]
            info.append(self.__sh(cmd, True))
            
        return info   
    
    def __getSystemInfo(self):
        
        info = ""
        info = p.node() + str(p.architecture()) + p.machine() + p.system() #+ str(uuid.getnode())
        
        return info
    
    def getFingerprinting(self,num=len(bios_cmd)):
        
        info = self.__getBiosInfo(num)
        info.append(self.__getSystemInfo())
        
        return info