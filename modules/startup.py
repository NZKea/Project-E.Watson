from modules.blockchain import avax_contract
import json

def setup_contracts(waiting_contracts):
    contract_file = open("./files/contracts.json")
    contracts_to_watch = json.load(contract_file)
    minted_addresses = open("./files/minted.txt").read().split(",")
    for address, contract in contracts_to_watch.items():
        if address in minted_addresses:
            print("Skipping:" + str(address) + " this address has been minted before (in seen.txt)" )
            continue
        else:
            try:
                waiting_contracts.append(avax_contract(address))
                print("Loaded " + contract["name"])
            except TypeError:
                print("Invalid Address loaded from json")
            except:
                print("Unexpected error in addresses in: ", address)
