from web3 import Web3
import requests


class avax_contract:
    def __init__(self, address, json):
        self.address = str(address)
        self.abi = requests.get("https://api.snowtrace.io/api?module=contract&action=getabi&address=" + address).json()["result"]
        self.contract = chain.eth.contract(Web3.toChecksumAddress(address), abi=self.abi)
        self.mint = json["mint_function"]
        self.trigger = json["trigger_function"]
        self.aggressiveness = str(json["aggressiveness"])
        self.max = json["max"]

    def call_no_inputs(self, function):
        return self.contract.functions[function]().call()

    def call(self, function, inputs):
        return self.contract.functions[function](inputs).call()

ANKR = 'https://rpc.ankr.com/avalanche'
chain = Web3(Web3.HTTPProvider(ANKR))