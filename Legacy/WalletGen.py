from web3 import Web3


def WalletGen() -> [str, str]:
    w3 = Web3()
    acc = w3.eth.account.create()

    private_key, public_key = w3.to_hex(acc._private_key), acc.address
    return [private_key, public_key]
