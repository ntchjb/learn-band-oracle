#!/bin/bash

OWNER=$OWNER
FROM=$FROM
NODE_IP=${NODE_IP:-localhost}
KEYRING=${KEYRING:-os}
CHAIN_ID=$CHAIN_ID
ORACLE_SCRIPT_ID=$ORACLE_SCRIPT_ID
MIN_COUNT=$MIN_COUNT
ASK_COUNT=$ASK_COUNT

bandd tx oracle request $ORACLE_SCRIPT_ID $ASK_COUNT $MIN_COUNT \
  -c "" \
  -m from_bandd \
  --keyring-backend $KEYRING \
  --from $FROM \
  --chain-id $CHAIN_ID \
  --fee-limit 32uband \
  --gas 2000000 \
  --prepare-gas 400000 \
  --execute-gas 600000 \
  --node "tcp://${NODE_IP}:26657"
