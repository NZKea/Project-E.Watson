from dotenv import load_dotenv, set_key
import json
import os

from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.shortcuts import message_dialog


def confirm_dialog(title, message):
    return yes_no_dialog(
        title=title,
        text=message).run()


def text_in_dialog(titles_messages):
    inputs = []
    for dialog in titles_messages:
        inputs.append(input_dialog(
            title=dialog[0],
            text=dialog[1]
            ).run())
    return inputs


def choice_dialog(title, message):
    return button_dialog(
        title=title,
        text=message,
        buttons = [
                  ('Done', None),
                  ('Add', True),
                  ('Clear All', False)
              ],
    ).run()

def address_builder(addresses, new):
    address_string = '['
    for address in addresses:
        address_string = address_string + '"' + address + '"' + ","
    address_string += '"' + str(new) + '"' + ']'
    return address_string


def set_env(new, name):
    os.environ[str(name)] = new
    set_key(".env", name, os.environ[str(name)])



# Wallets Config

def wallets_config():
    load_dotenv('.env')
    message_dialog(
        title='Warning',
        text='Info - there is no input validation on wallet addresses, this means you need to get them right').run()
    while True:
        wallet_addresses = (json.loads(os.getenv('wallet_addresses')))
        keys = (json.loads(os.getenv('keys')))
        wallet_choice = choice_dialog("Wallets", 'Your current wallets: ' + str(wallet_addresses))
        if wallet_choice:
            try:
                wallet_dialogs = text_in_dialog([["Address", "Address:"], ["Private Key", "Key:"]])
                new_wallet = wallet_dialogs[0]
                new_key = wallet_dialogs[1]
                if new_wallet and new_key:
                    set_env(address_builder(wallet_addresses, new_wallet), "wallet_addresses")
                    set_env(address_builder(keys, new_key), "keys")
            except:
                message_dialog("Failed", "Failed, check your inputs")
        elif wallet_choice == False:
            set_env('[]', "wallet_addresses")
            set_env('[]', "keys")
        else:
            break

# Contracts Config

class new_contract():
    def __init__(self, address, name, max, trigger_function, mint_function, aggressiveness):
        self.address = str(address).strip()
        self.name = str(name).strip()
        self.mint_function = str(mint_function)
        self.max = str(max).strip()
        self.trigger_function = trigger_function
        self.named_functions(trigger_function, mint_function)
        self.aggressiveness = int(aggressiveness)
        self.json = self.create_json()


    def named_functions(self, trigger_function, mint_function):
        if len(trigger_function) < 2:
            self.trigger_function = "allowlistStartTime"
        if len(mint_function) < 2:
            self.mint_function = "publicSaleMint"

    def create_json(self):
        return {
            self.address: {
                "name": self.name,
                "mint_function": self.mint_function,
                "max": self.max,
                "trigger_function": self.trigger_function,
                "aggressiveness": self.aggressiveness
            }
        }


def contracts_config():
    while True:
        with open("./files/contracts.json", "r+") as json_contract_list:
            contracts_list = json.load(json_contract_list)
            contract_choice = choice_dialog("Contracts", "Loaded contracts: " + str(contracts_list.keys()) )
            if contract_choice:
                try:
                    new_contract_input = text_in_dialog([["Address", "Contract Address"],["Name", "Name (use anything you want)"],["Max","Max amount e.g 1 (limit per wallet)"],["Trigger Func", "Contract Trigger Function Name without brackets - (returns either True or timestamp for start) (leave blank for Joepegs default)"],["Mint Func", "Contract Function Name without brackets  (leave blank for Joepegs default)"]])
                    aggressiveness = button_dialog(
                        title="Settings",
                        text="How aggressive should the minting transactions be?",
                        buttons=[('One tx', 1), ('Two txs', 2), ('Spam', 3)]).run()
                    contract = new_contract(new_contract_input[0], new_contract_input[1], new_contract_input[2], new_contract_input[3], new_contract_input[4], aggressiveness)
                    contracts_list.update(contract.json)
                except:
                    message_dialog("Error", "Failed to input details")
            elif contract_choice == False:
                contracts_list.clear()
                json_contract_list.truncate(0)
            else:
                break
            json_contract_list.seek(0)
            json.dump(contracts_list, json_contract_list)

