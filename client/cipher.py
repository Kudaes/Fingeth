from Crypto.Cipher import AES


def encrypt(data,key,iv):
    
    for i in range(len(iv)):
        cipher = AES.new(key,AES.MODE_CBC,iv[i])
        d = cipher.encrypt(data[i]) 
        data[i] = d
        
    return data

def decrypt(data,key,iv):
    
  
    for i in range(len(iv)):
        cipher = AES.new(key,AES.MODE_CBC,iv[i])
        d = cipher.decrypt(data[i]) 
        data[i] = d
      
    return data
