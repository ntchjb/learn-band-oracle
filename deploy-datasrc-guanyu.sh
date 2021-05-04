#!/bin/zsh

OWNER=$OWNER
FROM=$FROM
NODE_IP=${NODE_IP:-localhost}
KEYRING=${KEYRING:-os}
CHAIN_ID=$CHAIN_ID

bandcli tx oracle create-data-source --name "gold-freeforexapi.com" --description "get gold price in USD from freeforexapi.com" --script ./datasource-freeforexapi.com.py --owner $OWNER --from $FROM --keyring-backend $KEYRING --node "tcp://${NODE_IP}:26657" --chain-id $CHAIN_ID

bandcli tx oracle create-data-source --name "gold-goldprice.org" --description "get gold price in USD from goldprice.org" --script ./datasource-goldprice.org.py --owner $OWNER --from $FROM  --keyring-backend $KEYRING --node "tcp://${NODE_IP}:26657" --chain-id $CHAIN_ID

