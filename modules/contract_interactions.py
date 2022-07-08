import modules.mint as mint
from modules.utils import get_time


def check_timestamps(waiting_contracts, countdown_contracts):
    for contract in waiting_contracts:
        start_time = float(contract.call_no_inputs("allowlistStartTime"))
        if start_time > 0:
            waiting_contracts.remove(contract)
            countdown_contracts.append([contract, start_time])


def check_trigger(waiting_contracts, countdown_contracts):
    for contract in waiting_contracts:
        try:
            trigger_var = contract.call_no_inputs(contract.trigger)
            try:
                if trigger_var in ["True", "False"]:
                    trigger = bool(trigger_var)
                else:
                    trigger = float(trigger_var)
            except:
                print("Error checking trigger")
                break
            finally:
                if (type(trigger) is float and trigger > 0) or type(trigger) is bool:
                    waiting_contracts.remove(contract)
                    countdown_contracts.append([contract, trigger])
                else:
                    pass
        except:
            print("Invalid trigger function or contract")


mint_settings = {
    "1": {
        "repeats": 1,
        "delay": 0,
        "seconds_before": 0
    },
    "2": {
            "repeats": 2,
            "delay": 1,
            "seconds_before": 2
        },
    "3": {
            "repeats": 10,
            "delay": .75,
            "seconds_before": 5
            }
    }


def do_mint(countdown_contracts, contract):
    mint.rapid_multi_mint(contract[0], mint_settings)
    countdown_contracts.remove(contract)
    print("Attempted - check minted.txt")


def check_starting(countdown_contracts):
    for contract_and_trigger in countdown_contracts:
        seconds_before = mint_settings[contract_and_trigger[0].aggressiveness]["seconds_before"]
        if type(contract_and_trigger[1]) is float and contract_and_trigger[1] - get_time() < seconds_before:
            do_mint(countdown_contracts, contract_and_trigger)

        elif type(contract_and_trigger[1]) is bool:
            current_bool = contract_and_trigger[0].call_no_inputs(contract_and_trigger[0].trigger)
            if not bool(contract_and_trigger[1]) == bool(current_bool):
                do_mint(countdown_contracts, contract_and_trigger)

        else:
            print("Contract not ready")

