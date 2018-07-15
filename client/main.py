from controler import Controler

ctr = Controler()

def menu():
    
    inp = int(input("1- Register.\n2- Add new device\n3- Authenticate.\n4- Create fingerprint.\n5- Receive fingerprint.\n6- Exit.\n>"))
    return inp
      
def switch(num,values):
    print(values[num + 1])

def main():
    val = 0
    while(val != 6):
        val = menu()
        
        if val == 1:
            
            r = ctr.register()
            v = ["An error ocurred. Please try it again later.","Register completed.","You are already registered."]
            switch(r,v)
                
        elif val == 2:
            
            r = int(input("1- Add this devide.\m2- Read fingerprint file.\n>"))
            ret = 0
            if r == 1:
                ret = ctr.addDevice()
            elif r == 2:
                f = input("Select the fingerprint's file: ")
                ret = ctr.readAndAddDevice(f)
            else:
                print("Not a valid option.")
                ret = -1
            
            v = ["An error ocurred. Please try it again later.","Process completed."]
            switch(ret,v)               


        elif val == 3:
            
            r = ctr.authenticate()
            
            v = ["An error ocurred. Please try it again later.","Authenticated.","Authentication denied."]
            switch(r,v)

                
        elif val == 4:
            
                e = int(input("1- Export to txt file (default).\n2- Send to main node.\n>"))
                r = 0
                if e == 1:
                    r,f = ctr.exportFingerprint()                 
                    v = ["Error exporting fingerprint.","Fingerprint exported on " + f + "."]
                    switch(r,v)    
                elif e == 2:
                    ip = input("Insert remote IP address (be sure the node is listening):")
                    r = ctr.sendFingerprint(ip)
                    v = ["Error sending fingerprint to main node.","Fingerprint sent successfully."]
                    switch(r,v)           
                else:
                    print("Incorrect option.")
                                       
        elif val == 5:
            
            r = ctr.receiveFingerprint()
            v = ["An error ocurred. Please try it again later.","Success."]
            switch(r,v)                                
                    

if __name__ == "__main__":
    main()