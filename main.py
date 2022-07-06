#!/usr/bin/env python3

import time
import dotenv
import typer
import json
import os

from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt
from dotenv import load_dotenv

from modules import contract_interactions
from modules import startup
from modules.mint import load_env_vars


waiting_contracts = [] # Contract's without a start time
countdown_contracts = [] #Contracts with a start time


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


def text_in_dialog(title, message):
    return input_dialog(
        title=title,
        text=message).run()


def wallet_choice_dialog(title, message):
    return button_dialog(
        title=title,
        text=message,
        buttons = [
                  ('Done', None),
                  ('Add', True),
                  ('Clear All', False)
              ],
    ).run()


def wallet_address_builder(addresses, new_wallet):
    address_string = '\'['
    for address in addresses:
        address_string = address_string + '"' + address + '"' + ","
        print(address_string)
    address_string += '"' + str(new_wallet) + '"' + "]'"
    print(address_string)
    return address_string



@app.command()
def wallets():
    load_dotenv('.env')
    while True:
        wallet_addresses = (json.loads(os.getenv('test')))
        wallet_choice = wallet_choice_dialog("Wallets",'Your current wallets: ' + str(wallet_addresses))
        if wallet_choice:
            new_wallet = text_in_dialog("Address", "Address:")
            os.environ["test"] = wallet_address_builder(wallet_addresses, new_wallet)
            dotenv.set_key(".env", "test", os.environ["test"])
            text_in_dialog("Private Key", "Key:")
        elif wallet_choice == False:
            print("reset")
        else:
            break


@app.command()
def contracts():
    test = input("Hello")



if __name__ == "__main__":
    app()

