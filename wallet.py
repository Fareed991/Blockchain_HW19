
# import libraries
import subprocess
import json
import os
from constants import *
from dotenv import load_dotenv
from bipwallet import wallet
from web3 import Web3
from eth_account import Account
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

load_dotenv()



# import mnemonic from env
filepath="env.bat"
p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

stdout, stderr = p.communicate()
print (p.returncode) # is 0 if success
mnemonic = os.getenv('MNEMONIC')
print(mnemonic)



# connect to local ETH/ geth
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)





# Define function to derive wallet
def derive_wallets(mnemonic, coin, numderive):
    """Use the subprocess library to call the php file script from Python"""
    command = f'php /Users/fareedfreihat/Desktop/Homework19/Starter-Code/hd-wallet-derive/hd-wallet-derive.php -g --mnemonic="{mnemonic}" --numderive="{numderive}" --coin="{coin}" --format=json' 
    
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
   
    keys = json.loads(output)
    return  keys





# Test the function derive_wallets
derive_wallets(mnemonic, 'BTC', 3)




#Setting dictionary of coins to be used in the wallet
coins = {"eth", "btc-test", "btc"}
numderive = 3



 
keys = {}
for coin in coins:
    keys[coin]= derive_wallets(mnemonic, coin, numderive=3)





eth_PrivateKey = keys["eth"][0]['privkey']
btc_PrivateKey = keys['btc-test'][0]['privkey']

print(json.dumps(eth_PrivateKey, indent=4, sort_keys=True))
print(json.dumps(btc_PrivateKey, indent=4, sort_keys=True))




print(json.dumps(keys, indent=4, sort_keys=True))




# create a function that convert the privkey string in a child key to an account object.
def priv_key_to_account(coin,priv_key):
    print(coin)
    print(priv_key)
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)




def create_tx(coin,account, recipient, amount):
    if coin == ETH: 
        gasEstimate = w3.eth.estimateGas(
            {"from":eth_acc.address, "to":recipient, "value": amount}
        )
        return { 
            "from": eth_acc.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(eth_acc.address)
        }
    
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])



# create a function to hold Ethereum 
eth_acc = priv_key_to_account(ETH, derive_wallets(mnemonic, ETH,5)[0]['privkey'])




# create a function to send txn
def send_txn(coin,account,recipient, amount):
    txn = create_tx(coin, account, recipient, amount)
    if coin == ETH:
        signed_txn = eth_acc.sign_transaction(txn)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(result.hex())
        return result.hex()
    elif coin == BTCTEST:
        tx_btctest = create_tx(coin, account, recipient, amount)
        signed_txn = account.sign_transaction(txn)
        print(signed_txn)
        return NetworkAPI.broadcast_tx_testnet(signed_txn)


# ## BTC-TEST Transactions



btc_acc = priv_key_to_account(BTCTEST,btc_PrivateKey)




# create BTC transaction
create_tx(BTCTEST,btc_acc,"n3D8vVvLyD7pPQmWoQgMMERZrDjmBheBpU", 0.1)




# Send BTC transaction
send_txn(BTCTEST,btc_acc,"mtK73sNPY9CKuzVvpv4W1969AD1UmGGfsX", 0.1)


# ## ETH Transactions


#connecting to HTTP with address pk
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545/0xd36d0f9ff2f6dc80208cd19e0b7d939f11bd1a63d10c38cdc1c58f4dbbc95edc"))



# double check if  I am connected to blockchain. 
w3.isConnected()


# ## Check the Balance of the account with local mining blockchain



w3.eth.getBalance("0x5Ae99bfc31867F0c539ae4AE1aad61609f88ae78")




create_tx(ETH,eth_acc,"0x8b6A5A92B2cA4341c6827Eb70A66894Af33536B4", 1000)




send_txn(ETH, eth_acc,"0x8b6A5A92B2cA4341c6827Eb70A66894Af33536B4", 1)


# ## Confirmation of 



w3.eth.getBalance("0x8b6A5A92B2cA4341c6827Eb70A66894Af33536B4")