from os import path, remove
from iconsdk.wallet.wallet import KeyWallet

wallet1 = KeyWallet.create()
print("[wallet1] address: ", wallet1.get_address(), " private key: ", wallet1.get_private_key())

print(wallet1)


