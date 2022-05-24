# Incentive Helper

Helper to debug incentive assigned MoC to an account from the reward program.

**Requirement and installation**
 
* We need Python 3.6+
* Brownie
* Mongo db MoC Rewards (database)

Install libraries

`pip install -r requirements.txt`

[Brownie](https://github.com/eth-brownie/brownie) is a Python-based development and testing framework for smart contracts.
Brownie is easy so we integrated it with Money on Chain.

`pip install eth-brownie==1.16.0`

**Network Connections**

First we need to install custom networks (RSK Nodes) in brownie:

```
console> brownie networks add RskNetwork rskTestnetPublic host=https://public-node.testnet.rsk.co chainid=31 explorer=https://blockscout.com/rsk/mainnet/api
console> brownie networks add RskNetwork rskTestnetLocal host=http://localhost:4444 chainid=31 explorer=https://blockscout.com/rsk/mainnet/api
console> brownie networks add RskNetwork rskMainnetPublic host=https://public-node.rsk.co chainid=30 explorer=https://blockscout.com/rsk/mainnet/api
console> brownie networks add RskNetwork rskMainnetLocal host=http://localhost:4444 chainid=30 explorer=https://blockscout.com/rsk/mainnet/api
```

**Connection table**

| Network Name      | Network node          | Host                               | Chain    |
|-------------------|-----------------------|------------------------------------|----------|
| rskTestnetPublic   | RSK Testnet Public    | https://public-node.testnet.rsk.co | 31       |    
| rskTestnetLocal    | RSK Testnet Local     | http://localhost:4444              | 31       |
| rskMainnetPublic  | RSK Mainnet Public    | https://public-node.rsk.co         | 30       |
| rskMainnetLocal   | RSK Mainnet Local     | http://localhost:4444              | 30       |


### Usage

#### Incentive account

`python ./incentive_account.py`

Result:

|   Nº Block | Action   | MoC Rewarded   |   MoC Accumulated | BPro Holding   | Total BPro System   | Assign Date      |   User MoC Balance | Sent Amount   | Sent Date           |
|-----------:|:---------|:---------------|------------------:|:---------------|:--------------------|:-----------------|-------------------:|:--------------|:--------------------|
|    4268623 | assigned | 127.90         |           127.898 | 3.587153       | 407.186636          | 2022-04-28 00:12 |                0   |               |                     |
|    4271280 | assigned | 128.15         |           256.044 | 3.587153       | 406.397428          | 2022-04-29 00:11 |                0   |               |                     |
|    4273875 | assigned | 128.19         |           384.233 | 3.587153       | 406.260948          | 2022-04-30 00:11 |                0   |               |                     |
|    4275492 | sent     |                |             0     |                |                     |                  |            25437.9 | 25437.935725  | 2022-04-30 15:01:26 |
|    4276447 | assigned | 128.18         |           128.178 | 3.587153       | 406.296076          | 2022-05-01 00:11 |            25437.9 |               |                     |
|    4279064 | assigned | 128.29         |           256.469 | 3.587153       | 405.939236          | 2022-05-02 00:11 |            25437.9 |               |                     |
|    4281616 | assigned | 128.28         |           384.745 | 3.587153       | 405.986892          | 2022-05-03 00:11 |            25437.9 |               |                     |
