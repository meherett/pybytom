#!/usr/bin/env python3

from pybytom.transaction import Transaction, AdvancedTransaction
from pybytom.transaction.tools import spend_utxo_action, control_address_action
from pybytom.rpc import submit_transaction_raw
from pybytom.wallet import Wallet

import json

# Bytom network
NETWORK = "mainnet"  # mainnet, solonet & testnet
# 12 word mnemonic seed
MNEMONIC = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
# Bytom asset id
ASSET = "f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf"

# Initializing wallet
wallet = Wallet(network=NETWORK)
# Get Bytom wallet from mnemonic
wallet.from_mnemonic(mnemonic=MNEMONIC)
# Derivation from path
wallet.from_path("m/44/153/1/0/1")

# Initializing Transaction/AdvancedTransaction
# unsigned_advanced_transaction = Transaction(network=NETWORK)
unsigned_advanced_transaction = AdvancedTransaction(network=NETWORK)
# Building advanced transaction
unsigned_advanced_transaction.build_transaction(
    guid=wallet.guid(),
    inputs=[
        spend_utxo_action(
            utxo="d89449d3ec2117e4d2ad0f964f34a578cf8c980d049c273cb711f42378d734a3"
        )
    ],
    outputs=[
        control_address_action(
            asset=ASSET,
            amount=100,
            address=wallet.address()
        )
    ],
    fee=10_000_000,
    confirmations=1
)

print("Unsigned Advanced Transaction Fee:", unsigned_advanced_transaction.fee())
print("Unsigned Advanced Transaction Confirmations:", unsigned_advanced_transaction.confirmations())
print("Unsigned Advanced Transaction Hash:", unsigned_advanced_transaction.hash())
print("Unsigned Advanced Transaction Raw:", unsigned_advanced_transaction.raw())
print("Unsigned Advanced Transaction Json:", json.dumps(unsigned_advanced_transaction.json(), indent=4))
print("Unsigned Advanced Transaction Unsigned Datas:",
      json.dumps(unsigned_advanced_transaction.unsigned_datas(detail=False), indent=4))
print("Unsigned Advanced Transaction Signatures:", json.dumps(unsigned_advanced_transaction.signatures(), indent=4))

# Singing unsigned advanced transaction by xprivate key
signed_advanced_transaction = unsigned_advanced_transaction.sign(
    xprivate_key=wallet.xprivate_key(),
    account=1,  # Account index, default to 1
    change=False,  # Addresses for change False(0)/True(1), default to False(0)
    address=1,  # Address index, default to 1
    path="m/44/153/1/0/1",  # Derivation from path, default to None
    indexes=None  # Derivation from indexes, default to None
)

print("\nSigned Advanced Transaction Fee:", signed_advanced_transaction.fee())
print("Signed Advanced Transaction Confirmations:", signed_advanced_transaction.confirmations())
print("Signed Advanced Transaction Hash:", signed_advanced_transaction.hash())
print("Signed Advanced Transaction Raw:", signed_advanced_transaction.raw())
print("Signed Advanced Transaction Json:", json.dumps(signed_advanced_transaction.json(), indent=4))
print("Signed Advanced Transaction Unsigned Datas:",
      json.dumps(signed_advanced_transaction.unsigned_datas(detail=False), indent=4))
print("Signed Advanced Transaction Signatures:", json.dumps(signed_advanced_transaction.signatures(), indent=4))

# Submitting transaction raw
print("Bytom Blockchain Transaction Hash:", submit_transaction_raw(
    guid=wallet.guid(),
    transaction_raw=signed_advanced_transaction.raw(),
    signatures=signed_advanced_transaction.signatures(),
    network=NETWORK
))
