from pathlib import Path
import json
import web3
from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract
from Crypto.Hash import keccak
from Crypto import Random
import random
import string
import cipher
import base64
import ast  
from fingerprinting import FingerPrinter
from client_socket import ClientSocket
from finger_controler import FingerprintControler


class Controler():
    pathInfo = "./conf/contractInfo"
    pathContract = "./contract/contract.sol"
    pathProvider = ""
    pathIvs = "./conf/ivs"
    address = None
    abi = None
    numSalt = 6
    contract = None
    
    def __init__(self):
        my_provider = Web3.IPCProvider(self.pathProvider)
        self.w3 = Web3(my_provider)        
        self.w3.eth.defaultAccount = self.w3.eth.accounts[0]
        
        my_file = Path(self.pathInfo)
        if my_file.is_file():
            with open(my_file,'r') as f:
                self.address = f.readline().replace('\n','')
                self.abi = f.readline().replace('\n','')
                         
            self.contract = self.w3.eth.contract(
                address=self.address,
                abi=ast.literal_eval(self.abi),
            )        
      
    def __readContract(self):
        r = None
        my_file = Path(self.pathContract)
        if my_file.is_file():
            with open(my_file,'r') as f:
                r = f.read()
        else:
            raise IOError('Contract\'s file not found.')
        
        return r
        
    def __generateSalt(self):
        salt = []
        for i in range(self.numSalt):
            s = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(30))
            k = keccak.new(digest_bits=256)
            k.update(s.encode())
            salt.append(k.digest())
            
        return salt
    
    def __generateIvs(self):
        ivs = []
        for i in range(self.numSalt):   
            ivs.append(Random.new().read(cipher.AES.block_size))
        return ivs

    def __getPrivateKey(self):
        
        path = input('Insert your private key file\'s path:\n>')
        private_key = None
        with open(path,'r') as keyfile:
            encrypted_key = keyfile.read()
            password = input('Insert your ethereum account\'s password:\n>')
            try:
                private_key = self.w3.eth.account.decrypt(encrypted_key, password)
            except ValueError:
                print("Incorrect password.")
                raise ValueError('Invalid ethereum account\'s password.')
            
        return private_key
        
    def __generateFinalHash(self,hashes):
        
        k = keccak.new(digest_bits=256)        
        for i in range(len(hashes)):
            k.update(hashes[i])
            
        return k.digest() 
    
    def __generateParcialHashes(self,finger=None):

        pk = None
        while pk == None:
            try:
                pk = self.__getPrivateKey()
            except ValueError:
                pass
        
        ivs = []
        my_file = Path(self.pathIvs)
        if my_file.is_file():
            with open(my_file,'rb') as f:
                for i in range(self.numSalt):
                    iv = f.read(16)
                    ivs.append(iv)
        else:
            raise IOError('Ivs\'s file not found.')
        
        salt = self.contract.functions.getSalt().call()  #lo devuelve directamente en binario!        
        salt = cipher.decrypt(salt,pk,ivs)
        
        if finger == None:
            fp = FingerPrinter()
            finger = fp.getFingerprinting()
            
        hashes = []
        for i in range(self.numSalt):
            k = keccak.new(digest_bits=256)
            k.update(salt[i])
            k.update(finger[i].encode())
            hashes.append(k.digest()) 
            
        return hashes
        
    def register(self):
        
        if (self.address == None) or (self.abi == None):
            contract_source_code = None
            try:
                contract_source_code = self.__readContract()
            except IOError:
                return -1
            
            compiled = compile_source(contract_source_code,import_remappings=["-"]) # Compiled source code
            contract_interface = compiled['<stdin>:Log']       
            
            #Instantiate and deploy contract
            Log = self.w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
            
            salt = self.__generateSalt()
            pk = None
            while pk == None:
                try:
                    pk = self.__getPrivateKey()
                except ValueError:
                    pass
                
            ivs = self.__generateIvs()  

            salt = cipher.encrypt(salt,pk,ivs)

            
            # Submit the transaction that deploys the contract
            tx_hash = Log.constructor(salt).transact()
            
            # Wait for the transaction to be mined, and get the transaction receipt
            tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

            # Create the contract instance with the newly-deployed address
            self.contract = self.w3.eth.contract(
                address=tx_receipt.contractAddress,
                abi=contract_interface['abi'],
            )
                        
            
            if self.contract.functions.getElem().call() == 0:
                
                self.address = tx_receipt.contractAddress
                self.abi = contract_interface['abi']                
                my_file = Path(self.pathInfo)
                with open(my_file,'w') as f:  
                    f.write(tx_receipt.contractAddress + '\n')
                    f.write(str(contract_interface['abi']) + '\n')
                    
                my_file = Path(self.pathIvs)
                with open(my_file,'wb') as f:
                    for i in range(len(ivs)):
                        f.write(ivs[i])
                    
                return 0
            else:
                return -1
        else:           
            return 1
        
    def addDevice(self,f=None):
        
        hashes = None
        try:
            hashes = self.__generateParcialHashes(f)
        except IOError as e:
            print(e)
            return -1 
            
        
        h = self.__generateFinalHash(hashes)
        
        tx_hash = self.contract.functions.add(h).transact()
        
        # Wait for transaction to be mined...
        self.w3.eth.waitForTransactionReceipt(tx_hash)
        
        return 0
        
    def authenticate(self):
        
        try:
            hashes = self.__generateParcialHashes()
            sock = ClientSocket(self.address,self.abi,hashes)
            
        except IOError as e:
            print(e.message)
            return -1  

        
        return sock.authenticate()
    
    def exportFingerprint(self):
        
        finger = FingerPrinter()
        f = finger.getFingerprinting()   
        
        fctr = FingerprintControler()
        return fctr.exportFingerprint(f)
    
    def sendFingerprint(self,ip):
        
        finger = FingerPrinter()
        f = finger.getFingerprinting()  
        fctr = FingerprintControler()   
        
        return fctr.sendFingerprint(f,ip)
    
    def receiveFingerprint(self):
        
        ret = 0        
        fctr = FingerprintControler()
        f = fctr.receiveFingerprint()
        
        if f == None:
            return -1
        
        r = int(input("1- Export fingerprint to txt file.\n2- Add device to contract.\n>"))
    
        if r == 1:
            ret,f = fctr.exportFingerprint(f)            
        elif r == 2:
            ret = self.addDevice(f)
        else:
            ret = -1
        
        return ret
    
    def readAndAddDevice(self,f):
        
        fctr = FingerprintControler()
        finger = fctr.readFingeprint(f)
        
        return self.addDevice(finger)
        
        
