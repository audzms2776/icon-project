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

FROM = 'hxbfd31645a404f133241892215b27ba5f4d5e7202'
TO = 'hx79568e346607a1325f3ea2c0b2fbf66b9f1feee3'

def call_transfer(from_key, to_key, value):
    wallet1 = KeyWallet.load(from_key, 'qwer1234!')
    wallet2 = KeyWallet.load(to_key, 'qwer1234!')

# Generates an instance of transaction for sending icx.
# nid(network id); 1:mainnet, 2~:etc
    transaction = TransactionBuilder()\
        .from_(wallet1.get_address())\
        .to(wallet2.get_address())\
        .value(value)\
        .step_limit(100000000) \
        .nid(3) \
        .nonce(2) \
        .version(3) \
        .timestamp(int(time() * 10 ** 6))\
        .build()

# Returns the signed transaction object having a signature
    signed_transaction = SignedTransaction(transaction, wallet1)

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


