#!/usr/bin/env python3
import requests
import sys
import os
import typing

from bech32 import bech32_encode, bech32_decode

BECH32_PUBKEY_ACC_PREFIX = "bandpub"
BECH32_PUBKEY_VAL_PREFIX = "bandvaloperpub"
BECH32_PUBKEY_CONS_PREFIX = "bandvalconspub"

BECH32_ADDR_ACC_PREFIX = "band"
BECH32_ADDR_VAL_PREFIX = "bandvaloper"
BECH32_ADDR_CONS_PREFIX = "bandvalcons"

URL = "https://asia-southeast2-price-caching.cloudfunctions.net/query-price"
HEADERS = {"Content-Type": "application/json"}

def test_bech32():
    testBechStr = "band1m5lq9u533qaya4q3nfyl6ulzqkpkhge9q8tpzs"
    hrp, bz = bech32_decode(testBechStr)
    assert hrp == BECH32_ADDR_ACC_PREFIX, "Invalid bech32 prefix"
    assert bz is not None, "result should not be empty"

    result = bech32_encode(BECH32_ADDR_VAL_PREFIX, bz)
    assert result == "bandvaloper1m5lq9u533qaya4q3nfyl6ulzqkpkhge9v30z8m", "invalid encoding"


def main(symbols):
    try:
        payload = {"source": "cmc", "symbols": symbols}
        # test bech32 usage
        test_bech32()
        pxs = requests.request("POST", URL, headers=HEADERS, json=payload).json()
        if len(pxs) != len(symbols):
            raise Exception("PXS_AND_SYMBOL_LEN_NOT_MATCH")
        return ",".join(pxs)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        print(main([*sys.argv[1:]]))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)