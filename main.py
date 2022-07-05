#!/usr/bin/env python3

import time
import json
import os


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


load_env_vars()
startup.setup_contracts(waiting_contracts)
main_loop()




