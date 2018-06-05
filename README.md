# cointree-python-sdk
An SDK for the Cointree exchange API 

## Setup
Set environment variables:
COINTREE_API_KEY = "<your_api_key>"
COINTREE_SECRET_KEY = "<your_precious_secret>" 

## Example Usage
'''python
from cointree import Cointree

c = Cointree()
c.get_price('btc', 'aud') 

>>> {'ask': 10342.00, 'spot': 10342.00, 'bid': 10211.00}

