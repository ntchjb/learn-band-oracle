#!/bin/zsh

RUSTFLAGS='-C link-arg=-s' cargo build --release --target wasm32-unknown-unknown

bandd tx oracle create-oracle-script --name "Gold Price" --description "get gold prices in USD and average them" --script ./target/wasm32-unknown-unknown/release/learn_owasm.wasm --owner band1m5lq9u533qaya4q3nfyl6ulzqkpkhge9q8tpzs --from requester --keyring-backend test --node "tcp://localhost:26657" --chain-id bandchain --schema "{multiplier:u64}/{price:u64}" --gas 1000000
