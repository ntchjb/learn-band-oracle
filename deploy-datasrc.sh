#!/bin/zsh

bandd tx oracle create-data-source --name "gold-freeforexapi.com" --description "get gold price in USD from freeforexapi.com" --script ./datasource-freeforexapi.com.py --owner band1m5lq9u533qaya4q3nfyl6ulzqkpkhge9q8tpzs --from devnet-admin --keyring-backend test --node "tcp://rpc-master.d3n.xyz:26657" --chain-id bandchain
bandd tx oracle create-data-source --name "gold-goldprice.org" --description "get gold price in USD from goldprice.org" --script ./datasource-goldprice.org.py --owner band1m5lq9u533qaya4q3nfyl6ulzqkpkhge9q8tpzs --from devnet-admin --keyring-backend test --node "tcp://rpc-master.d3n.xyz:26657" --chain-id bandchain
