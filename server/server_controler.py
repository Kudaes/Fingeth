import web3
from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract
import string
import ast  


class ServerControler():
    pathProvider = "/root/Desktop/blockchain1/geth.ipc"
    DEL = "[*]"
    
    
    def __init__(self,adr,abi,hashes):
        my_provider = Web3.IPCProvider(self.pathProvider)
        self.w3 = Web3(my_provider)        
        self.w3.eth.defaultAccount = self.w3.eth.accounts[0]
        self.address = adr
        self.abi = abi 
        self.contract = self.w3.eth.contract(
            address=self.address,
            abi=ast.literal_eval(self.abi),
        )
        
        self.h = hashes.split(self.DEL)
        for i in range(len(self.h)):
            self.h[i] = bytes.fromhex(self.h[i])
      
    
    
    def authenticate(self):
        
        if self.contract.functions.check(self.h).call():
            return 0
        else:
            return 1