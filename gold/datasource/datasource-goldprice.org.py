#!/usr/bin/env python3
from decimal import Decimal, getcontext
import requests
import sys

URL = "https://data-asg.goldprice.org/dbXRates/USD"

def main(symbols):
    try:
        pxs = requests.get(URL, headers={'User-Agent': 'curl/7.64.1'}).json()
        return Decimal(pxs['items'][0]['xauPrice'])
    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        print('{0:.2f}'.format(main([*sys.argv[1:]])))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)