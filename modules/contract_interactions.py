import modules.mint as mint
from modules.utils import get_time


def check_timestamps(waiting_contracts, countdown_contracts):
    for contract in waiting_contracts:
        start_time = float(contract.call_no_inputs("allowlistStartTime"))
        if start_time > 0:
            waiting_contracts.remove(contract)
            countdown_contracts.append([contract, start_time])


def check_starting(countdown_contracts):
    seconds_before = 10
    for contract in countdown_contracts:
        if contract[1] - get_time() < seconds_before:
            mint.rapid_multi_mint(contract[0], .75, 25)
            countdown_contracts.remove(contract)
            print("Attempted - check minted.txt")
