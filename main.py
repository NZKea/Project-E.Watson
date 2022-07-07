#!/usr/bin/env python3

import time
import dotenv
import typer
import json
import os
from web3 import Web3

from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.shortcuts import message_dialog

from dotenv import load_dotenv

from modules import contract_interactions
from modules import startup
from modules.mint import load_env_vars


waiting_contracts = [] # Contract's without a start time
countdown_contracts = [] # Contracts with a start time


def main_loop():
    while True:
        contract_interactions.check_timestamps(waiting_contracts, countdown_contracts)
        if len(countdown_contracts) == 0:
            time.sleep(30)
        else:
            contract_interactions.check_starting(countdown_contracts)
            time.sleep(1)
            contract_interactions.check_starting(countdown_contracts)



def restart_contracts():
    startup.setup_contracts(waiting_contracts)


app = typer.Typer()

@app.command()
def start():
    load_env_vars()
    startup.setup_contracts(waiting_contracts)
    main_loop()



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
    dotenv.set_key(".env", name, os.environ[str(name)])



@app.command()
def wallets():
    load_dotenv('.env')
    message_dialog(
        title='Warning',
        text='Info - there is no input validation on wallet addresses, this means you need to get them right').run()
    while True:
        wallet_addresses = (json.loads(os.getenv('wallet_addresses')))
        keys = (json.loads(os.getenv('wallet_addresses')))
        wallet_choice = choice_dialog("Wallets",'Your current wallets: ' + str(wallet_addresses))
        if wallet_choice:
            try:
                wallet_dialogs = text_in_dialog([["Address", "Address:"], ["Private Key", "Key:"]])
                new_wallet = wallet_dialogs[0]
                new_key = wallet_dialogs[1]
                if new_wallet and new_key:
                    set_env(address_builder(wallet_addresses, new_wallet), "wallet_addresses")
                    set_env(address_builder(keys, new_key), "keys")
            except:
                message_dialog("Failed","Failed, check your inputs")
        elif wallet_choice == False:
            set_env('[]', "wallet_addresses")
        else:
            break

class new_contract():
    def __init__(self, address, name, price, max, trigger_function, mint_function):
        self.address = str(address).strip()
        self.name = str(name).strip()
        self.price = str(price).strip()
        self.mint_function = str(mint_function)
        self.max = str(max).strip()
        self.trigger_function = trigger_function
        self.named_functions(trigger_function, mint_function)
        self.json = self.create_json()
    
    def named_functions(self,trigger_function, mint_function):
        if len(trigger_function) < 2:
            self.trigger_function = "allowlistStartTime"
        if len(mint_function) < 2:
            self.mint_function = "publicSaleMint"

    def create_json(self):
        return {
            self.address: {
                "name": self.name,
                "price": self.price,
                "mint_function": self.mint_function,
                "max": self.max,
                "trigger_function": self.trigger_function
            }
        }


@app.command()
def contracts():
    while True:
        with open("files/contracts.json","r+") as json_contract_list:
            contracts_list = json.load(json_contract_list)
            contract_choice = choice_dialog("Contracts", "Loaded contracts: " + str(contracts_list.keys()) )
            if contract_choice:
                try:
                    new_contract_input = text_in_dialog([["Address", "Contract Address"],["Name", "Name (use anything you want)"],["Price","Price digit (0 for free)"],["Max","Max amount e.g 1 (limit per wallet)"],["Trigger Func", "Contract Trigger Function Name - (a function that returns either True or timestamp for start) (leave blank for Joepegs default)"],["Mint Func", "Contract Function Name (leave blank for Joepegs default)"]])
                    contract = new_contract(new_contract_input[0], new_contract_input[1], new_contract_input[2], new_contract_input[3], new_contract_input[4],new_contract_input[5])
                    contracts_list.update(contract.json)
                except:
                    message_dialog("Error", "Failed to input details")
                contract = new_contract(new_contract_input[0], new_contract_input[1], new_contract_input[2], new_contract_input[3], new_contract_input[4],new_contract_input[5])
            elif contract_choice == False:
                contracts_list.clear()
                json_contract_list.truncate(0)
            else:
                break
            json_contract_list.seek(0)
            json.dump(contracts_list, json_contract_list)


if __name__ == "__main__":
    app()

