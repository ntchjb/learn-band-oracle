#!/usr/bin/env python3
import ccxt
import ccxt.async_support as async_ccxt
import aiohttp
import asyncio
import statistics
import sys


async def coingecko():
    async with aiohttp.ClientSession() as session:
        res = await session.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "tether", "vs_currencies": "usd"},
        )
        return (await res.json())["tether"]["usd"]


async def cryptocompare():
    async with aiohttp.ClientSession() as session:
        res = await session.get(
            "https://min-api.cryptocompare.com/data/price",
            params={"fsym": "USDT", "tsyms": "USD"},
        )
        return (await res.json())["USD"]


async def last_price(exchange):
    instance = getattr(async_ccxt, exchange)()
    try:
        data = await instance.fetch_ticker("USDT/USD")
        return data["last"]
    finally:
        await instance.close()


def get_usdt():
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(coingecko()),
        loop.create_task(cryptocompare()),
        loop.create_task(last_price("kraken")),
        loop.create_task(last_price("bitfinex")),
        loop.create_task(last_price("ftx")),
    ]
    loop.run_until_complete(
        asyncio.wait([asyncio.gather(*tasks, return_exceptions=True)], timeout=3)
    )
    results = []
    for t in tasks:
        if t.done() and not t.exception():
            results.append(float(t.result()))
    return statistics.median(results)


def adjust_rounding(data):
    if data < 1:
        return round(data, 8)
    elif data < 10:
        return round(data, 6)
    else:
        return round(data, 4)


def main(data):
    exchange_name = data[0]
    symbols = []
    convert_usdt = False
    exchange = getattr(ccxt, exchange_name)()
    if exchange.has["fetchTickers"]:
        if (
            exchange_name == "binance"
            or exchange_name == "huobipro"
            or exchange_name == "okex"
            or exchange_name == "hitbtc"
        ):
            convert_usdt = True
            symbols = [(symbol.upper() + "/USDT") for symbol in data[1:]]
        elif exchange_name == "bithumb" or exchange_name == "coinone":
            symbols = [(symbol.upper() + "/KRW") for symbol in data[1:]]
        elif exchange_name == "bibox":
            convert_usdt = True
            exchange.has["fetchCurrencies"] = False
            symbols = [(symbol.upper() + "/USDT") for symbol in data[1:]]
        else:
            symbols = [(symbol.upper() + "/USD") for symbol in data[1:]]
        tickers = exchange.fetchTickers(symbols)
        result = [
            (str(px["last"]), symbol)
            for px in list(tickers.values())
            for symbol in symbols
            if symbol == px["symbol"]
        ]
        rates = [
            float(res[0]) for symbol in symbols for res in result if res[1] == symbol
        ]
        if convert_usdt:
            usdt = get_usdt()
            rates = [(rate * usdt) for rate in rates]
        return ",".join([str(adjust_rounding(rate)) for rate in rates])
    else:
        raise ValueError(
            "exchange {} does not support multiple tickers".format(exchange_name)
        )


if __name__ == "__main__":
    try:
        print(main([*sys.argv[1:]]))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)