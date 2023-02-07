from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
# with open("simpleStorage.sol", "a+") as file:
with open("simpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
# compile
compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"simpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
# print(compile_sol)
with open("compliled_code.json", "w") as file:
    json.dump(compile_sol, file)


# get bytecode
# bytecode = (
#     compile_sol["contracts"]["simpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"][
#         "object"
#     ],
# )

# print(bytecode)
# get abi
abi = compile_sol["contracts"]["simpleStorage.sol"]["SimpleStorage"]["abi"]
# print(abi)
# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 5777
my_address = "0xabf271B85Ea50e8988927E9c35Effb1DFbdca957"
private_key = "0x5ed6df69a01d40eab0f897a6e97668137ad51c96e9b549b7bb2150f5d18303d0"
account2 = "0x00715e3fE7EE89cb1DF68E4805FcBb6e5Bf6F4a9"
# private_key = "your_private_key"
# private_key = os.getenv('PRIVATE_KEY')
# print(private_key)
# dotenv.config() to load the environment variables from your env file, then accessing the environment variable using process.env.VARIABLE_NAME. For example, if the private key is stored in the environment variable PRIVATE_KEY, then you can access it with const privateKey = process.env.PRIVATE_KEY.
# hex_string = private_key.replace("[^0-9A-Fa-f]", "PRIVATE_EY")


bytecode = w3.eth.get_code(my_address)
# create a contract in python
SimpleStorage = w3.eth.contract(address=my_address, abi=abi, bytecode=bytecode)
# SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)
# print(SimpleStorage)
#  get latest transaction
# nonce = w3.eth.getTransactionCount(my_address)
nonce = w3.eth.get_transaction_count(my_address, "latest")
# print(Web3.to_wei)
# print(nonce)

# Building a transaction
# 1.Build the transaction deploy
# 2.sign in a transaction
# 3.send the transaction
gas_price = w3.to_wei('50', 'gwei')
current_balance = w3.eth.get_balance(my_address)
# print(current_balance)

# amount_in_wei= w3.eth.to_wei()
# amount_to_wei = w3.toWei(1, 'ether')
# amount_in_wei = w3.eth.toWei(1, 'ether'
amount_in_wei = w3.to_wei(1, 'ether')
# w3.eth.send_transaction({
#     "from":my_address ,
#     "to":account2,
#     "value":amount_in_wei
#     })
# print(amount_in_wei)




transaction = SimpleStorage.constructor().build_transaction({
    "from": my_address,
    #  "to": my_address,
     "nonce": nonce ,
     "gasPrice" : gas_price , 
     "value":amount_in_wei
     })

# print("TRANSACTION ... ")
# print(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction , private_key = private_key).rawTransaction
# print(signed_txn)

tx_hash = w3.eth.send_raw_transaction(signed_txn)
# print(tx_hash)
#wait for block confirmation
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
if  w3.is_connected():
 print("my web3 is connected")  
else: 
    print("it is not connected")
# this is to get all block of the transaction
# blockchain_info =w3.eth.get_block('latest')
# print(blockchain_info)

# working with the contracts
# we need contract address and contract abi

simple_storage = w3.eth.contract(address= tx_receipt.contractAddress , abi = abi)
# call -> simulate making the call and getting return value 
# calling is just assimilation
# transact actually make state change
# calling view function
# print(simple_storage.functions.retrieve().call())
print(simple_storage.functions.store(15).call())
# storing transaction
store_transaction = simple_storage.functions.store(15).build_transaction(
    {"chain_id":chain_id ,"from":my_address ,"nonce": nonce +1}
    # nonce should be used once that why i used +1
)
signed_store_tx = w3.eth.sign_transaction(
    store_transaction, private_key = private_key
)
print(signed_store_tx)
# send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
# tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
 



