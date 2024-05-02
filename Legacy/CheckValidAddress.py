from web3 import Web3


def CheckValidAddress(str) -> bool:
    w3 = Web3()
    return w3.is_address(str)
