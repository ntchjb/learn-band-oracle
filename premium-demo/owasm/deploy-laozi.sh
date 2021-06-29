#!/bin/bash

OWNER=$OWNER
FROM=$FROM
KEYRING=${KEYRING:-os}
NODE_IP=${NODE_IP:-localhost}
CHAIN_ID=$CHAIN_ID

RUSTFLAGS='-C link-arg=-s' cargo build \
  --release \
  --target wasm32-unknown-unknown

bandd tx oracle create-oracle-script \
  --name "CoinGecko (Premium Demo)" \
  --description "get cryptocurrency prices in USD" \
  --script ./target/wasm32-unknown-unknown/release/coingecko.wasm \
  --owner $OWNER  \
  --from $FROM \
  --keyring-backend $KEYRING \
  --node "tcp://${NODE_IP}:26657" \
  --chain-id $CHAIN_ID \
  --schema "{endpoint:string,symbols:[string],multiplier:u64}/{price:[u64]}" \
  --gas 1000000
