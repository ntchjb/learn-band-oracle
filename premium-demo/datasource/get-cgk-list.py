import requests

duplicates = {
  "compound-coin": 1, "farmatrust": 1, "freetip": 1, "blocktrade": 1, "eldorado-token": 1,
  "payperex": 1, "stox": 1, "menlo-one": 1, "one": 1, "one-hundred-coin-2": 1,
  "financex-exchange": 1, "firstenergy-token": 1, "u-os-network": 1, "hinto": 1, "hymnode": 1,
  "hotnow": 1, "hydro-protocol": 1, "beats-token": 1, "genesis-coin": 1, "spartancoin": 1,
  "unipump": 1, "cannadrix": 1, "bitsou": 1, "tradekax": 1, "futurexcrypto": 1,
  "mykey": 1, "key": 1, "groovyhooman": 1, "penta": 1, "uni-coin": 1,
  "unicorn-token": 1, "universe-token": 1, "lina": 1, "platoncoin": 1, "wrapped-terra": 1,
  "bat-true-share": 1, "mir-coin": 1, "yottachainmena": 1, "golden-ratio-token": 1, "socketfinance": 1,
  "obitan-chain": 1, "thorchain-erc20": 1, "bolt-true-share": 1, "linear-bsc": 1, "evolution": 1,
  "momo-key": 1, "bittup": 1, "trebit-network": 1, "anoncoin": 1, "aragon-china-token": 1,
  "binance-peg-uniswap": 1, "cube": 1, "antcoin": 1, "binance-peg-dogecoin": 1, "binance-peg-iotex": 1,
  "uservice": 1, "wrapped-ust-bsc": 1, "aave-eth-v1": 1, "fitmin": 1, "one-token": 1,
}

symbols = {
  'BTC': 1, 'ETH': 1, 'USDT': 1, 'XRP': 1, 'LINK': 1, 'DOT': 1, 'BCH': 1, 'LTC': 1, 'ADA': 1, 'BSV': 1,
  'CRO': 1, 'BNB': 1, 'EOS': 1, 'XTZ': 1, 'TRX': 1, 'XLM': 1, 'ATOM': 1, 'XMR': 1, 'OKB': 1, 'USDC': 1,
  'NEO': 1, 'XEM': 1, 'LEO': 1, 'HT': 1, 'VET': 1, 'YFI': 1, 'MIOTA': 1, 'LEND': 1, 'SNX': 1, 'DASH': 1,
  'COMP': 1, 'ZEC': 1, 'ETC': 1, 'OMG': 1, 'MKR': 1, 'ONT': 1, 'NXM': 1, 'AMPL': 1, 'BAT': 1, 'THETA': 1,
  'DAI': 1, 'REN': 1, 'ZRX': 1, 'ALGO': 1, 'FTT': 1, 'DOGE': 1, 'KSM': 1, 'WAVES': 1, 'EWT': 1, 'DGB': 1,
  'KNC': 1, 'ICX': 1, 'TUSD': 1, 'SUSHI': 1, 'BTT': 1, 'BAND': 1, 'EGLD': 1, 'ANT': 1, 'NMR': 1, 'PAX': 1,
  'LSK': 1, 'LRC': 1, 'HBAR': 1, 'BAL': 1, 'RUNE': 1, 'YFII': 1, 'LUNA': 1, 'DCR': 1, 'SC': 1, 'STX': 1,
  'ENJ': 1, 'BUSD': 1, 'OCEAN': 1, 'RSR': 1, 'SXP': 1, 'BTG': 1, 'BZRX': 1, 'SRM': 1, 'SNT': 1, 'SOL': 1,
  'CKB': 1, 'BNT': 1, 'CRV': 1, 'MANA': 1, 'YFV': 1, 'KAVA': 1, 'MATIC': 1, 'TRB': 1, 'REP': 1, 'FTM': 1,
  'TOMO': 1, 'ONE': 1, 'WNXM': 1, 'PAXG': 1, 'WAN': 1, 'SUSD': 1, 'RLC': 1, 'OXT': 1, 'RVN': 1, 'FNX': 1,
  'RENBTC': 1, 'WBTC': 1, 'DIA': 1, 'BTM': 1, 'IOTX': 1, 'FET': 1, 'JST': 1, 'MCO': 1, 'KMD': 1, 'BTS': 1,
  'QKC': 1, 'YAMV2': 1, 'XZC': 1, 'UOS': 1, 'AKRO': 1, 'HNT': 1, 'HOT': 1, 'KAI': 1, 'OGN': 1, 'WRX': 1,
  'KDA': 1, 'ORN': 1, 'FOR': 1, 'AST': 1, 'STORJ': 1, 'TWOKEY': 1, 'ABYSS': 1, 'BLZ': 1, 'BTU': 1, 'CND': 1,
  'CVC': 1, 'DGX': 1, 'ELF': 1, 'EQUAD': 1, 'EURS': 1, 'FXC': 1, 'GDC': 1, 'GEN': 1, 'GHT': 1, 'GNO': 1,
  'GVT': 1, 'IOST': 1, 'KEY': 1, 'LOOM': 1, 'MET': 1, 'MFG': 1, 'MLN': 1, 'MTL': 1, 'MYB': 1, 'NEXXO': 1,
  'NPXS': 1, 'OST': 1, 'PAY': 1, 'PBTC': 1, 'PLR': 1, 'PLTC': 1, 'PNK': 1, 'PNT': 1, 'POLY': 1, 'POWR': 1,
  'QNT': 1, 'RAE': 1, 'REQ': 1, 'RSV': 1, 'SAN': 1, 'SPIKE': 1, 'SPN': 1, 'STMX': 1, 'TKN': 1, 'TKX': 1,
  'TRYB': 1, 'UBT': 1, 'UPP': 1, 'USDS': 1, 'VIDT': 1, 'XHV': 1, 'CREAM': 1, 'UNI': 1, 'LINA': 1, 'XVS': 1,
  'UMA': 1, 'CELO': 1, 'QTUM': 1, 'HYN': 1, 'ZIL': 1, 'ZB': 1, 'FIL': 1, 'ALPHA': 1, 'TWT': 1,
}

def main():
  coins = requests.get('https://api.coingecko.com/api/v3/coins/list').json()
  result = {}
  for coin in coins:
    if (coin['id'] not in duplicates) and (coin['symbol'].upper() in symbols):
      result[coin['symbol'].upper()] = coin['id']
  
  for symbol in symbols:
    if symbol not in result:
      print(symbol)
  print(result)
  

if __name__ == "__main__":
  main()
