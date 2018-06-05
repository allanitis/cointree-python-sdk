import base64
import hmac
import hashlib
import json
import os
from time import time

from botocore.vendored import requests

class Cointree(object):
    def __init__(self):
        """
        set some defaults
        """
        self._api_key = os.environ['COINTREE_API_KEY']
        self._api_secret = os.environ['COINTREE_SECRET_KEY']
        self._endpoint = "https://api.cointree.com.au/v1"
        self._logging = "cointree.log"

    ### Util
    def _post_request(self, endpoint):
        """Post with credentials."""
        sig = self._generate_signature()
        return requests.post(endpoint, params={'key': self._api_key, 'nonce': sig[1], 'signature': sig[0]})

    def _get_request(self, endpoint):
        """Get with credentials."""
        sig = self._generate_signature()
        return requests.get(endpoint, params={'key': self._api_key, 'nonce': sig[1], 'signature': sig[0]})

    def _delete_request(self, endpoint):
        """Delete with credentials."""
        sig = self._generate_signature()
        return requests.delete(endpoint, params={'key': self._api_key, 'nonce': sig[1], 'signature': sig[0]})

    def _generate_signature(self):
        """Generate hmac signature with unix time nonce."""
        epoch = str(int(time()))
        return (base64.b64encode(hmac.new(self._api_secret.encode('utf-8'), epoch.encode('utf-8'), digestmod=hashlib.sha256).digest()), epoch)

    ### APIs
    def get_price(self, primary_coin, secondary_coin):
        """Get the buy, spot, and sell price of bitcoin."""
        return self._get_request(self._endpoint + f'/price/{primary_coin}/{secondary_coin}')

    def get_altcoin_price(self, coin):
        """Get the price of an altcoin related to bitcoin."""
        return self._get_request(self._endpoint + f'/price/btc/{coin}')

    def get_altcoin_list(self):
        """Get the list of available altcoins."""
        return self._get_request(self._endpoint + '/price/altcoins')

    def get_account_details(self):
        """Account details including balance, reserved balance, and deposit address."""
        return self._get_request(self._endpiont + '/account')

    def get_account_history(self):
        """The history of transactions for the account."""
        return self._get_request(self._endpoint + '/account/log')

    def get_purchase_history(self, type):
        """
        List the current and previous purchases on the account.

        type: buys, sells
        """
        return requests.get(self._endpoint + f'/account/{type}')

    def make_order(self, type, amount, method='online'):
        """
        Make an order for BTC for a certain price.

        type: buy, sells
        amount: decimal amount in AUD
        """
        return requests.post(self._endpoint + f'/account/altcoins?altcoin={altcoin}&amount={amount}&method={method}')

    def cancel_order(self, type, reference):
        """
        Cancel an order than hasn't yet been processed.

        type: buy, sells
        reference: the trade reference number
        """
        return self._delete_request(self._endpoint + f'/account/{type}?reference={reference}')

    def get_altcoin_purchsae_history(self):
        """List the current and previous altcoin purchases."""
        return self._get_request(self._endpoint + '/account/altcoins')

    def purchase_altcoin(self, altcoin, amount, addr, txt=None):
        """Purchase an altcoin with BTC."""
        return self._post_request(self._endpoint + f'/account/altcoins?=altcoin={altcoin}&amount={amount}&address={addr}&field1={txt}')

    def cancel_purchase_altcoin(self, reference):
        """Cancel an altcoin order that hasn't yet been processed."""
        return self._delete_request(self._endpoint + f'/account/altcoins?reference={reference}')

    def get_sends(self):
        """List the current and previous bitcoin transfers from your account."""
        return self._get_request(self._endpoint + '/account/sends')

    def send_btc(self, dest, amount, priority=False):
        """Send bitcoin from your account to another wallet."""
        return self._post_request(self._endpoint + f'/account/sends?destination={dest}&amount={amount}&highpriority={priority}')

    def cancel_send(self, reference):
        """Cancel a bitcoin transfer that hasn't yet been processed."""
        return self._delete_request(self._endpoint + f'/account/sends?reference={reference}')

    def get_bill_payments(self):
        """List the current and previous bill payments from your account."""
        return self._get_request(self._endpoint + '/account/payments')

    def create_bill_payment(self, biller, reference, amount):
        """Create a new bill payment to another biller."""
        return self._post_request(self._endpoint + f'/account/payments?billercode={biller}&customerreference={reference}&amount={amount}')

    def cancel_bill_payment(self, reference):
        """Cancel a bill payment that hasn't yet been processed."""
        return self._delete_request(self._endpoint + f'/account/payments?reference={reference}')


if __name__ == "__main__":
    c = Cointree()
    print(c.get_price('btc', 'aud').text)
    # p = c.get_purchase_history('buys')
    # print(p.text)
