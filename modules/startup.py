from modules.blockchain import avax_contract
import json

def setup_contracts(waiting_contracts):
    contract_file = open("./files/contracts.json")
    contracts_to_watch = json.load(contract_file)
    minted_addresses = open("./files/minted.txt").read().split(",")
    for address, json_contract in contracts_to_watch.items():
        if address in minted_addresses:
            print("Skipping:" + str(address) + " this address has been minted before (in seen.txt)" )
            break
        else:
            try:
                waiting_contracts.append(avax_contract(address, json_contract))
                print("Loaded " + json_contract["name"] + " " + address + ' each mint tx will try mint ' + json_contract["max"] + "for " + json_contract["price"] + " avax")
            except TypeError:
                print("Invalid Address loaded from json")
            except:
                print("Unexpected error in addresses: ", address)
