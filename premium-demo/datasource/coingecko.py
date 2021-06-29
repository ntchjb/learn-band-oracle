#!/usr/bin/env python3
import requests
import sys
import os
import typing

# List of supported coins based on Band's standard price reference
COINS_LIST = {
  "BTG": "bitcoin-gold",
  "BZRX": "bzx-protocol",
  "SRM": "serum",
  "SNT": "status",
  "SOL": "solana",
  "CKB": "nervos-network",
  "BNT": "bancor",
  "CRV": "curve-dao-token",
  "MANA": "decentraland",
  "KAVA": "kava",
  "MATIC": "matic-network",
  "TRB": "tellor",
  "REP": "augur",
  "FTM": "fantom",
  "TOMO": "tomochain",
  "ONE": "harmony",
  "WNXM": "wrapped-nxm",
  "PAXG": "pax-gold",
  "WAN": "wanchain",
  "SUSD": "nusd",
  "RLC": "iexec-rlc",
  "FNX": "finnexus",
  "WBTC": "wrapped-bitcoin",
  "DIA": "dia-data",
  "BTM": "bytom",
  "IOTX": "iotex",
  "FET": "fetch-ai",
  "JST": "just",
  "KMD": "komodo",
  "BTS": "bitshares",
  "QKC": "quark-chain",
  "YAMV2": "yam-v2",
  "AKRO": "akropolis",
  "KAI": "kardiachain",
  "OGN": "origin-protocol",
  "WRX": "wazirx",
  "KDA": "kadena",
  "FOR": "force-protocol",
  "AST": "airswap",
  "STORJ": "storj",
  "2KEY": "2key",
  "ABYSS": "the-abyss",
  "BLZ": "bluzelle",
  "BTU": "btu-protocol",
  "CND": "cindicator",
  "CVC": "civic",
  "DGX": "digix-gold",
  "ELF": "aelf",
  "EQUAD": "quadrant-protocol",
  "EURS": "stasis-eurs",
  "FXC": "futurexcrypto",
  "GDC": "global-digital-content",
  "GEN": "daostack",
  "GHT": "global-human-trust",
  "GNO": "gnosis",
  "GVT": "genesis-vision",
  "IOST": "iostoken",
  "KEY": "selfkey",
  "LOOM": "loom-network",
  "MET": "metronome",
  "MLN": "melon",
  "MTL": "metal",
  "MYB": "mybit-token",
  "NEXXO": "nexxo",
  "NPXS": "pundi-x",
  "OST": "simple-token",
  "PAY": "tenx",
  "PBTC": "ptokens-btc",
  "PLR": "pillar",
  "PLTC": "ptokens-ltc",
  "PNK": "kleros",
  "PNT": "penta,pnetwork",
  "POLY": "polymath-network",
  "POWR": "power-ledger",
  "QNT": "quant-network",
  "RAE": "rae-token",
  "REQ": "request-network",
  "RSV": "reserve",
  "SAN": "santiment-network-token",
  "SPIKE": "spiking",
  "SPN": "sapien,spartancoin",
  "STMX": "storm",
  "TKN": "tokencard",
  "TKX": "tokenize-xchange",
  "TRYB": "bilira",
  "UBT": "unibright",
  "UPP": "sentinel-protocol",
  "USDS": "stableusd",
  "VIDT": "v-id-blockchain",
  "CAKE": "pancakeswap-token",
  "CREAM": "cream-2",
  "UNI": "uniswap",
  "FIL": "filecoin",
  "ALPHA": "alpha-finance",
  "TWT": "trust-wallet-token",
  "UOS": "ultra",
  "HNT": "helium,hymnode",
  "HOT": "holotoken",
  "ORN": "orion-protocol",
  "MFG": "syncfab",
  "SXP": "swipe",
  "RENBTC": "renbtc",
  "BNB": "binancecoin",
  "ETH": "ethereum",
  "BTC": "bitcoin",
  "LINA": "lina,linear",
  "XVS": "venus",
  "BSV": "bitcoin-cash-sv",
  "CRO": "crypto-com-chain",
  "XMR": "monero",
  "OKB": "okb",
  "NEO": "neo",
  "XEM": "nem",
  "LEO": "leo-token",
  "HT": "huobi-token",
  "VET": "vechain",
  "MIOTA": "iota",
  "LEND": "ethlend",
  "SNX": "havven",
  "DASH": "dash",
  "COMP": "compound-governance-token",
  "ZEC": "zcash",
  "ETC": "ethereum-classic",
  "OMG": "omisego",
  "MKR": "maker",
  "ONT": "ontology",
  "NXM": "nxm",
  "AMPL": "ampleforth",
  "BAT": "basic-attention-token",
  "THETA": "theta-token",
  "REN": "republic-protocol",
  "ZRX": "0x",
  "ALGO": "algorand",
  "FTT": "ftx-token",
  "DOGE": "dogecoin",
  "KSM": "kusama",
  "WAVES": "waves",
  "EWT": "energy-web-token",
  "DGB": "digibyte",
  "KNC": "kyber-network",
  "ICX": "icon",
  "TUSD": "true-usd",
  "SUSHI": "sushi",
  "BTT": "bittorrent-2",
  "EGLD": "elrond-erd-2",
  "ANT": "aragon",
  "NMR": "numeraire",
  "PAX": "paxos-standard",
  "LSK": "lisk",
  "BCH": "bitcoin-cash",
  "LTC": "litecoin",
  "USDT": "tether",
  "BAND": "band-protocol",
  "DAI": "dai",
  "EOS": "eos",
  "XTZ": "tezos",
  "ATOM": "cosmos",
  "USDC": "usd-coin",
  "TRX": "tron",
  "XRP": "ripple",
  "LINK": "chainlink",
  "DOT": "polkadot",
  "YFI": "yearn-finance",
  "XLM": "stellar",
  "ADA": "cardano",
  "BUSD": "binance-usd",
  "LRC": "loopring",
  "HBAR": "hedera-hashgraph",
  "BAL": "balancer",
  "RUNE": "thorchain",
  "YFII": "yfii-finance",
  "LUNA": "terra-luna",
  "DCR": "decred",
  "SC": "siacoin",
  "STX": "blockstack,stox",
  "ENJ": "enjincoin",
  "OCEAN": "ocean-protocol",
  "RSR": "reserve-rights-token",
  "BTU": "btu-protocol",
  "FRAX": "frax",
  "OXT": "orchid-protocol",
  "XHV": "haven",
  "COVER": "cover-protocol",
  "AAVE": "aave",
  "HEGIC": "hegic",
  "SFI": "saffron-finance",
  "KP3R": "keep3rv1",
  "RVN": "ravencoin",
  "SCRT": "secret",
  "STRK": "strike",
  "INDEX": "index-cooperative",
  "PERP": "perpetual-protocol",
  "DPI": "defipulse-index",
  "ANC": "anchor-protocol",
  "MIR": "mirror-protocol",
  "VAI": "vai",
  "UMA": "uma",
  "CELO": "celo",
  "QTUM": "qtum",
  "ZIL": "zilliqa",
  "MVL": "mass-vehicle-ledger",
  "ARPA": "arpa-chain",
  "AUTO": "auto",
  "UST": "terrausd",
  "AETH": "ankreth",
  "DEFI++": "piedao-defi",
  # Extra token
  "BTCB": "bitcoin-bep2",
  "BETH": "binance-eth",
}

HEADERS = {"Content-Type": "application/json"}

# Reads values from Yoda Executor's environment variables
def set_header_from_env(headers: typing.Dict[str, str], key: str):
  value = os.environ.get(key)
  if value != None:
    headers[key] = value

# Create request verification info as HTTP headers
def set_request_verification_headers(existingHeaders: typing.Dict[str, str]) -> typing.Dict[str, str]:
  newHeaders = existingHeaders.copy()
  set_header_from_env(newHeaders, "BAND_CHAIN_ID")
  set_header_from_env(newHeaders, "BAND_VALIDATOR")
  set_header_from_env(newHeaders, "BAND_REQUEST_ID")
  set_header_from_env(newHeaders, "BAND_EXTERNAL_ID")
  set_header_from_env(newHeaders, "BAND_REPORTER")
  set_header_from_env(newHeaders, "BAND_SIGNATURE")
  return newHeaders

# Convert symbols to coin IDs based on `/coins/list` of CoinGecko
def get_ids_from_symbols(symbols: typing.List[str]) -> typing.List[str]:
  ids = []
  for symbol in symbols:
    if symbol in COINS_LIST:
      ids.append(COINS_LIST[symbol])
  return ids

# This data source receives 2 arguments.
# The first argument is Gateway's endpoint, which is used for testing purpose only.
# The seconds argument is a string of comma-separated symbols
def main(endpoint, raw_symbols):
  # Prepare request verification info 
  headers = set_request_verification_headers(HEADERS)

  # Get coin IDs to query price from CoinGecko
  symbols = raw_symbols.split(",")
  ids = get_ids_from_symbols(symbols)
  params = { "ids": ids }

  # Send GET request to Premium Data Source's Gateway
  r = requests.get(endpoint, headers=headers, params=params)
  r.raise_for_status()

  # Receive a response constructed by your own implementation of the Gateway
  # For this case, the response is an arrray of coin prices
  # ordered respectively to given symbols
  pxs = r.json()
  if len(pxs) != len(symbols):
    raise Exception("PXS_AND_SYMBOL_LEN_NOT_MATCH")

  # Construct the result to be handled by Oracle Script
  # For this case, the result should be comma-separated
  return ",".join(pxs)

if __name__ == "__main__":
  try:
    print(main(sys.argv[1], sys.argv[2]))
  except Exception as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)
