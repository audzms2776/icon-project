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
from rere import retry


icon_service = IconService(HTTPProvider('http://localhost:9000/api/v3'))

wallet1 = KeyWallet.load(bytes.fromhex('5da628d4aa9636e888458d2b9b4bf65726b9f25363b8f43d482442ab66b5f822'))
print("[wallet1] address: ", wallet1.get_address(), " private key: ", wallet1.get_private_key())

# Generates an instance of transaction for sending icx.
# nid(network id); 1:mainnet, 2~:etc
transaction = TransactionBuilder()\
    .from_(wallet1.get_address())\
    .to('hx1000000000000000000000000000000000000000')\
    .value(10)\
    .step_limit(100000000) \
    .nid(3) \
    .nonce(2) \
    .version(3) \
    .timestamp(int(time() * 10 ** 6))\
    .build()

# Returns the signed transaction object having a signature
signed_transaction = SignedTransaction(transaction, wallet1)

# Reads params to transfer to nodes
print("\nparams: ")
pprint(signed_transaction.signed_transaction_dict)

# Sends the transaction
tx_hash = icon_service.send_transaction(signed_transaction)
print("txHash: ", tx_hash)

@retry(JSONRPCException, tries=10, delay=1, back_off=2)
def get_tx_result():
    # Returns the result of a transaction by transaction hash
    tx_result = icon_service.get_transaction_result(tx_hash)
    print("\ntransaction status(1:success, 0:failure): ", tx_result["status"])

    # Gets balance
    balance = icon_service.get_balance(wallet1.get_address())
    print("balance: ", balance, "\n")


get_tx_result()


