from icon_transaction import call_transfer
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from flask import Flask,request


icon_service = IconService(HTTPProvider('http://localhost:9000/api/v3'))
app = Flask(__name__)


# call_transfer('key1', 'key2', 100)

def show_balance():
    key_arr  = ['key1', 'key2', 'place1', 'place2', 'place3']

    for key in key_arr:
        wallet = KeyWallet.load(key, "qwer1234!")
        print(key, icon_service.get_balance(wallet.get_address()))


@app.route('/transfer', methods=['POST'])
def home():
    req_json = request.get_json()

    from_key = req_json['from']
    to_key = req_json['to']
    value = req_json['value']

    call_transfer(from_key, to_key, value)
    print(from_key + ' -->' + to_key + ' :: ' + str(value) + '\n')
    show_balance()

    return '123123'


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
