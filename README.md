# learn-band-oracle

This tutorial presents methods and steps to create, build and test bandchain's oracle script and data sources. The example provided in this repository is two data sources providing gold price in USD and oracle script that takes the gold prices from different external data sources and validators to calculate average of the price.

## Prerequisite

1. Rust nightly build 1.49 (2020-10-08) (nightly version is required by dynasm lib)
2. Python3

## Data sources

Data source need to be able to run as executable e.g. `./gold-price USD`. In this example, we can run the data source by following commands.

- `./datasource-freeforexapi.com`
- `./datasource-goldprice.org`

Note that validators need to have runtime for the data source's executable. (e.g. `python3`). It will then return a single number to the console representing current gold price in USD dollars.

In order to store data source to Bandchain network, we need to send a Transaction using `MsgCreateDataSource`. In order to send the transaction, we use CLI command as follow

```sh
bandcli tx oracle create-data-source \
--name "data source name" \
--description "data source description" \
--script "./path/to/datasource/file" \
--owner "bandAddress1a2b3c4d..." \
--from "cosmos-keyring-name" \
--keyring-backend "keyring backend name" \
--node "tcp://node-to-be.used:26657" \
--chain-id "band-guanyu-testnet3"
```

Now, after running the command above, data source will be uploaded to Bandchain. It will be run off-chain once requesting data from the sources is needed.

## Oracle Script

Oracle script is a script written in Rust which will be compiled to WebAssembly target. In order to compile the script, the command need to target on `wasm32-unknown-unknown` platform, as shown below.

```sh
RUSTFLAGS='-C link-args=-s' cargo build --target wasm32-unknown-unknown --release
```

Now, we have got `.wasm` executable file in target folder. Next, we need a string of OBI spec that is indicated in the script. This can be done by running test by run the command `cargo test -- --nocapture`.

After we got executable file and OBI schema, we are ready to submit it to Bandchain network. It can be done in similar way as submitting data souces.

```sh
bandcli tx oracle create-oracle-script \
--name "oracle script name" \
--description "oracle script description" \
--script target/wasm32-unknown-unknown/release/learn_owasm.wasm \
--owner "bandAddress1a2b3c4d..." \
--schema "{multiplier:u64}/{price:u64}" \
--url "https://ipfs.io/ipfs" \
--from "cosmos-keyring-name" \
--keyring-backend "keyring backend name" \
--node "tcp://node-to-be.used:26657" \
--chain-id "band-guanyu-testnet3"
--gas 1000000
```

Please note that gas amount should be indicated to provide sufficient amount of gas to be able to run transaction.

That's it! Happy Coding :)
