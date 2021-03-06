#!/bin/zsh

OWNER=$OWNER
FROM=$FROM
NODE_IP=${NODE_IP:-localhost}
KEYRING=${KEYRING:-os}
CHAIN_ID=$CHAIN_ID
ORACLE_SCRIPT_ID=$ORACLE_SCRIPT_ID
MIN_COUNT=$MIN_COUNT
ASK_COUNT=$ASK_COUNT

bandcli tx oracle request $ORACLE_SCRIPT_ID $ASK_COUNT $MIN_COUNT \
  -c "0000000000000064" \
  -m from_bandd \
  --from $FROM \
  --chain-id $CHAIN_ID \
  --gas 3000000 \
  --node tcp://$NODE_IP:26657 \
  --keyring-backend $KEYRING
