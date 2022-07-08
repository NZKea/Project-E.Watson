#!/usr/bin/env python3

import time
import typer

from modules.configs import wallets_config, contracts_config
from modules import contract_interactions
from modules import startup
from modules.mint import load_env_vars

app = typer.Typer()
waiting_contracts = [] # Contract's without a start time
countdown_contracts = [] # Contracts with a start time


def main_loop():
    while True:
        contract_interactions.check_trigger(waiting_contracts, countdown_contracts)
        if len(countdown_contracts) == 0:
            time.sleep(30)
        else:
            contract_interactions.check_starting(countdown_contracts)
            time.sleep(1)
            contract_interactions.check_starting(countdown_contracts)

def restart_contracts():
    startup.setup_contracts(waiting_contracts)

@app.command()
def start():
    load_env_vars()
    startup.setup_contracts(waiting_contracts)
    main_loop()


@app.command()
def wallets():
    wallets_config()


@app.command()
def contracts():
    contracts_config()


if __name__ == "__main__":
    app()

