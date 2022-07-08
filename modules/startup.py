from modules.blockchain import avax_contract
import json

def setup_contracts(waiting_contracts):
    contract_file = open("./files/contracts.json")
    contracts_to_watch = json.load(contract_file)
    minted_addresses = open("./files/minted.txt").read().split(",")
    for address, json_contract in contracts_to_watch.items():
        if address.lower() in minted_addresses:
            print("Skipping:" + str(address) + " this address has been minted before (in seen.txt)" )
            continue
        else:
            try:
                waiting_contracts.append(avax_contract(address, json_contract))
                try:
                    print("Loaded " + json_contract["name"] + " " + address + ' each mint tx will try mint ' + json_contract["max"])
                except:
                    print("A contract was loaded but not all of its attributes could be read.  May cause issue check contracts.json for mistakes")
            except TypeError:
                print("Invalid Address loaded from json")
            except:
                print("Unexpected error in addresses: ", address)
