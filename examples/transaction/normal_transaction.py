#!/usr/bin/env python3

from pybytom.transaction import NormalTransaction
from pybytom.rpc import submit_transaction_raw
from pybytom.wallet import Wallet

import json

# Bytom network
NETWORK = "mainnet"  # Choose mainnet, solonet or testnet
# 12 word mnemonic seed
MNEMONIC = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
# Bytom asset id
ASSET_ID = "f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf"

# Initializing wallet
wallet = Wallet(network=NETWORK)
# Get Bytom wallet from mnemonic
wallet.from_mnemonic(mnemonic=MNEMONIC)
# Derivation from path
wallet.from_path("m/44/153/1/0/1")

# Initializing normal transaction
unsigned_normal_transaction = NormalTransaction(network=NETWORK)
# Building normal transaction
unsigned_normal_transaction.build_transaction(
    guid=wallet.guid(),
    recipients={
        "bm1qzx7pjr6whcaxmh9u0thkjuavf2ynk3zkgshhle": 10_000_000_000
    },
    asset=ASSET_ID
)

print("Unsigned Normal Transaction Fee:", unsigned_normal_transaction.fee())
print("Unsigned Normal Transaction Confirmations:", unsigned_normal_transaction.confirmations())
print("Unsigned Normal Transaction Hash:", unsigned_normal_transaction.hash())
print("Unsigned Normal Transaction Raw:", unsigned_normal_transaction.raw())
print("Unsigned Normal Transaction Json:", json.dumps(unsigned_normal_transaction.json(), indent=4))
print("Unsigned Normal Transaction Unsigned Datas:",
      json.dumps(unsigned_normal_transaction.unsigned_datas(detail=False), indent=4))
print("Unsigned Normal Transaction Signatures:", json.dumps(unsigned_normal_transaction.signatures(), indent=4))

# Singing unsigned normal transaction by xprivate key
signed_normal_transaction = unsigned_normal_transaction.sign(
    xprivate_key=wallet.xprivate_key(),
    account=1,  # Account index, default to 1
    change=False,  # Addresses for change False(0)/True(1), default to False(0)
    address=1,  # Address index, default to 1
    path=None,  # Derivation from path, default to None
    indexes=None  # Derivation from indexes, default to None
)

print("\nSigned Normal Transaction Fee:", signed_normal_transaction.fee())
print("Signed Normal Transaction Confirmations:", signed_normal_transaction.confirmations())
print("Signed Normal Transaction Hash:", signed_normal_transaction.hash())
print("Signed Normal Transaction Raw:", signed_normal_transaction.raw())
print("Signed Normal Transaction Json:", json.dumps(signed_normal_transaction.json(), indent=4))
print("Signed Normal Transaction Unsigned Datas:",
      json.dumps(signed_normal_transaction.unsigned_datas(detail=False), indent=4))
print("Signed Normal Transaction Signatures:", json.dumps(signed_normal_transaction.signatures(), indent=4))

# Submitting transaction raw
print("Submitted Bytom Blockchain Transaction Hash:", submit_transaction_raw(
    guid=wallet.guid(),
    transaction_raw=signed_normal_transaction.raw(),
    signatures=signed_normal_transaction.signatures(),
    network=NETWORK
))
