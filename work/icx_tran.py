from time import sleep, time
from pprint import pprint

from iconsdk.wallet.wallet import KeyWallet
from iconsdk.builder.transaction_builder import TransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.exception import JSONRPCException
from iconsdk.utils.convert_type import convert_hex_str_to_int
from iconsdk.builder.call_builder import CallBuilder


icon_address =  "cxe962408ca9158161572b28196637729778b6a01d" 

wallet1 = KeyWallet.load(bytes.fromhex('dd90fe8e8961ad5e28b1b3c787f684ed935198162762c5bfa986f3f46aabd4b4'))
print("[wallet1] address: ", wallet1.get_address(), " private key: ", wallet1.get_private_key())


wallet2 = KeyWallet.create()
print("[wallet2] address: ", wallet2.get_address(), " private key: ", wallet2.get_private_key())

icon_service = IconService(HTTPProvider('http://localhost:9000/api/v3'))


call = CallBuilder().from_(wallet1.get_address())\
                    .to(icon_address)\
                    .params({"_owner": wallet1.get_address()})\
                    .method("balanceOf")\
                    .build()

# Executes a call method to call a read-only API method on the SCORE immediately without creating a transaction on Loopchain
result = icon_service.call(call)

print(result)


