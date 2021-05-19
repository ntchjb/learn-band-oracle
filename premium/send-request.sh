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
  -c "0000005d68747470733a2f2f617369612d736f75746865617374322d62616e642d706c617967726f756e642e636c6f756466756e6374696f6e732e6e65742f70726963652d63616368696e672d726571756573742d766572696669636174696f6e00000002000000034254430000000442414e440000000000000064" \
  -m from_bandd \
  --keyring-backend $KEYRING \
  --from $FROM \
  --chain-id $CHAIN_ID \
  --fee-limit 32uband \
  --gas 1000000