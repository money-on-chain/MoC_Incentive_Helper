# Incentive Helper

Helper to debug incentive assigned MoC to an account from the reward program.

**Requirement and installation**
 
* We need Python 3.6+
* Mongo db stable

Install libraries

`pip install -r requirements.txt`

### Usage

#### Incentive account

edit `config.json` or paste information from json file in `settings` folder  

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
