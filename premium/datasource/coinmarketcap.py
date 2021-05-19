#!/usr/bin/env python3
import requests
import sys
import os
import typing

HEADERS = {"Content-Type": "application/json"}

def set_header_from_env(headers: typing.Dict[str, str], key: str):
    value = os.environ.get(key)
    if value != None:
        headers[key] = value

def set_request_verification_headers(existingHeaders: typing.Dict[str, str]) -> typing.Dict[str, str]:
    newHeaders = existingHeaders.copy()
    set_header_from_env(newHeaders, "BAND_CHAIN_ID")
    set_header_from_env(newHeaders, "BAND_VALIDATOR")
    set_header_from_env(newHeaders, "BAND_REQUEST_ID")
    set_header_from_env(newHeaders, "BAND_EXTERNAL_ID")
    set_header_from_env(newHeaders, "BAND_REPORTER")
    set_header_from_env(newHeaders, "BAND_SIGNATURE")
    return newHeaders

def main(endpoint, raw_symbols):
    symbols = raw_symbols.split(",")
    payload = {"source": "cmc", "symbols": symbols}
    headers = set_request_verification_headers(HEADERS)
    r = requests.post(endpoint, headers=headers, json=payload)
    r.raise_for_status()
    pxs = r.json()

    if len(pxs) != len(symbols):
        raise Exception("PXS_AND_SYMBOL_LEN_NOT_MATCH")
    rates = []
    for symbol in symbols:
        rates.append(str(pxs[symbol]))

    return ",".join(rates)


if __name__ == "__main__":
    try:
        print(main(sys.argv[1:]))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
