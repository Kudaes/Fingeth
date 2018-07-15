pragma solidity ^0.4.24;
contract Mortal {

    address owner;

    function Mortal() public { owner = msg.sender; }

    function kill() public { require(msg.sender == owner); selfdestruct(owner); }
}

contract Log is Mortal {

    mapping(uint256 => bytes32) log;
    bytes32[] salt; //sales encriptadas 
    uint256 numElem;
    uint128 numHashes;


    /* This runs when the contract is executed */
    function Log (bytes32[] a) public Mortal(){
        numElem = 0;
        numHashes = 6;
        for(uint256 i = 0; i < a.length;i ++){
            salt.push(a[i]);
        }
    }
    
    function check(bytes32[] a) public view returns (bool){
        
        if (a.length != numHashes){return false;}
        
        bytes32 d = keccak256(abi.encodePacked(a));
        
        for(uint256 i = 0; i < numElem; i++){
           if(log[i] == d){
               return true;
           }
        }
        return false;
        
    }
    
    function add(bytes32 a) public {
        
        require(msg.sender == owner);
        for(uint256 i = 0; i < numElem; i++){
           if(log[i] == a){
               return;
           }
        }
        
        log[numElem] = a;
        numElem ++;

    }
    
    function getSalt() public view returns (bytes32[]){
        return salt;
    }
    
    function getElem() public view returns (uint256){
        return numElem;
    }
    
    function getNumHash() public view returns (uint128){
        return numHashes;
    }
    function getHash(uint256 e) public view returns (bytes32){
        return log[e];
    }
    
   
}
