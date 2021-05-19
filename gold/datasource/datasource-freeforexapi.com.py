#!/usr/bin/env python3
from decimal import Decimal, getcontext
import requests
import sys

URL = "https://www.freeforexapi.com/api/live?pairs=USDXAU"

def main(symbols):
    try:
        pxs = requests.get(URL).json()
        return Decimal(1) / Decimal(pxs['rates']['USDXAU']['rate'])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        print('{0:.2f}'.format(main([*sys.argv[1:]])))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)