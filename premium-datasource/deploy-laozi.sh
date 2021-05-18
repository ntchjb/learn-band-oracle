#!/bin/bash

OWNER=$OWNER
FROM=$FROM
NODE_IP=${NODE_IP:-localhost}
KEYRING=${KEYRING:-os}
CHAIN_ID=$CHAIN_ID

bandd tx oracle create-data-source --name "CoinMarketCap" --description "get currencies from coinmarketcap.com" --script ./coinmarketcap.py --owner $OWNER --from $FROM --keyring-backend $KEYRING --node "tcp://${NODE_IP}:26657" --chain-id $CHAIN_ID --treasury $OWNER --fee 2uband
