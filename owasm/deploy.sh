#!/bin/zsh

cd ./owasm && RUSTFLAGS='-C link-arg=-s' cargo build --release --target wasm32-unknown-unknown && cd ../

bandd tx oracle create-oracle-script --name "Gold Price" --description "get gold prices in USD and average them" --script ./target/wasm32-unknown-unknown/release/learn_owasm.wasm --owner band1m5lq9u533qaya4q3nfyl6ulzqkpkhge9q8tpzs --from devnet-admin --keyring-backend test --node "tcp://rpc-master.d3n.xyz:26657" --chain-id bandchain --schema "{multiplier:u64}/{price:u64}" --gas 1000000
