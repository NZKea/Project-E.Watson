import time
from web3 import Web3
from dotenv import load_dotenv
import json
import os

from modules.blockchain import chain


def load_env_vars():
    global keys
    global bot_addresses
    load_dotenv('.env')
    bot_addresses = []
    keys = json.loads(os.getenv('keys'))
    for address in json.loads(os.getenv('wallet_addresses')):
        try:
            bot_addresses.append(Web3.toChecksumAddress(address))
        except ValueError:
            print("Invalid address for", address)
        except:
            print("Unexpected error passing wallet addresses", address)


def mint(contract, key, address):
    nonce = chain.eth.get_transaction_count(address)
    mint_txn = contract.contract.functions.publicSaleMint(
        1
    ).buildTransaction({
        #'chainId': 98000,
        'gas': 152883,
        'maxFeePerGas': Web3.toWei('73', 'gwei'),
        'maxPriorityFeePerGas': Web3.toWei('1', 'gwei'),
        'nonce': nonce,
    })
    signed_tx = chain.eth.account.sign_transaction(mint_txn, private_key=key)
    sent_tx = chain.eth.send_raw_transaction(signed_tx.rawTransaction)


def rapid_multi_mint(contract, delay, repeats):
    for repeat in range(repeats):
        print(keys)
        for i, key in enumerate(keys):
            try:
                mint(contract, key, bot_addresses[i])
            except IndexError:
                print("Check that private keys and addresses match")
            except:
                print("Unknown minting error")
        time.sleep(delay)
    attempted_mint_list = open("./files/minted.txt", "a")
    attempted_mint_list.write(contract.address + ",")
    attempted_mint_list.close()
