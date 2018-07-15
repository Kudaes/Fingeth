# Fingeth

Python fingerprint authentication PoC using Ethereum's blockchain and smart contracts.

## Getting Started

These instructions will get you a copy of the project up and running on your local Ubuntu machine for development and testing purposes. This project is just a PoC and should never be implemented in real enviroments. 

### Prerequisites

Install Go implementation of the Ethereum protocol (geth).

```
sudo apt-get install software-properties-common
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install ethereum
```

Install solidity compiler.

```
sudo apt-get install solc
```

Install python dependencies.

```
pip3 install -r requirements.txt
```

### Installing

First of all you have to setup your own private Ethereum network. Create your custom Genesis  file to initiate it. Be sure your network ID is random enough to be "unique" (otherwise external nodes may find your network).

Genesis file example:

```
{
    "config": {  
        "chainId": 123456789,  
        "homesteadBlock": 0,
        "eip155Block": 0,
        "eip158Block": 0
    },
    "difficulty": "0x400",
    "gasLimit": "0x8000000000",  
    "alloc": {
    	"0000000000000000000000000000000000000001": {
          "balance": "1"
	    },
	    "0000000000000000000000000000000000000002": {
	      "balance": "1"
	    },
	    "0000000000000000000000000000000000000003": {
	      "balance": "1"
	    },
	    "0000000000000000000000000000000000000004": {
	      "balance": "1"
	    }
    }
}

```

Open a terminal and start your network.

```
geth --identity "youridentity" init /path/to/your/CustomGenesis.json --datadir /path/to/your/blockchaindir
geth --datadir --datadir /path/to/your/blockchaindir --networkid 123456789
```
After that open a new terminal and type in:

```
geth attach /path/to/your/blockchaindir/geth.ipc
```
You will get a Javascript console connected to your Ethereum node. After that you have to create an account in order to interact with the network. We will use this account to deploy contracts to the network and register our fingerprints.

```
personal.newAccount()
personal.unlockAccount(web3.eth.accounts[0],'yourpassword',0) // This will unlock permanently your account
miner.start() // Get some ether. Use miner.stop() to stop mining.  
```
Remember you need at least one node in the network mining each time you create a new transaction (deploying contracts or adding new fingerprints).

Repeat previous steps in another machine if you want to have more than one node in your network and also if you want to prove the authentication running client and server in separated machines.

Finally, remember to update the value of variable "pathProvider" in /client/controler.py to point to your ipc file. 

## Testing the tool

Start the tool in both client and server machine.

Client side: 

```
python3 main.py
```
Server side:

```
python3 server_main.py
```

Now that the server is listening, just deploy your contract and register your device's fingerprint by selecting:

```
1- Register.
2- Add new device.
	2.1- Add this device.
3- Authenticate.
```

If everything went right you will get an "Authenticated" message.


### Add new fingerprints to your contract

You may want to authenticate with more than one device. To do that just follow the installation steps in your new machine.

After that, you can generate your new device's fingerprint ("Create fingerprint") and send it to your main node ("Send/Receive fingerprint") to update your contract or just export it to a txt file.

Remember that in order to add more than one fingerprint to the same contract you only will be able to do it with the Ethereum account used to deploy the contract.



## Built With

* [Ethereum](https://www.ethereum.org/) 
* [Python 3](https://www.python.org/download/releases/3.0/) 
* [Geth](https://geth.ethereum.org/) - Go implementation of the Ethereum protocol


## License

This project is licensed under the GPL v3 License - see the [License.md](License.md) file for details.

