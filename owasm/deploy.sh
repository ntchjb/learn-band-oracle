#!/bin/zsh

OWNER=$OWNER
FROM=$FROM
KEYRING=${KEYRING:-os}
NODE_IP=${NODE_IP:-localhost}
CHAIN_ID=$CHAIN_ID

RUSTFLAGS='-C link-arg=-s' cargo build --release --target wasm32-unknown-unknown

bandd tx oracle create-oracle-script --name "Gold Price" --description "get gold prices in USD and average them" --script ./target/wasm32-unknown-unknown/release/learn_owasm.wasm --owner $OWNER  --from $FROM --keyring-backend $KEYRING --node "tcp://${NODE_IP}:26657" --chain-id $CHAIN_ID --schema "{multiplier:u64}/{price:u64}" --gas 1000000
