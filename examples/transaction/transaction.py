#!/usr/bin/env python3

from pybytom.wallet import Wallet
from pybytom.assets import BTM as ASSET
from pybytom.transaction import Transaction
from pybytom.transaction.tools import find_p2wsh_utxo
from pybytom.transaction.actions import (
    spend_utxo, control_address
)
from pybytom.rpc import submit_transaction_raw
from typing import Optional

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"  # Default is mainnet
# Bytom sidechain (Vapor protocol)
VAPOR: bool = False  # Default is False
# Wallet mnemonic words
MNEMONIC: str = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
# Secret passphrase/password for mnemonic
PASSPHRASE: Optional[str] = None  # str("meherett")
# Wallet derivation path
PATH: str = "m/44/153/1/0/1"

# Initialize Bytom wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Bytom wallet from mnemonic
wallet.from_mnemonic(mnemonic=MNEMONIC, passphrase=PASSPHRASE)
# Derivation from path
wallet.from_path(path=PATH)

# Initialize Bytom transaction
unsigned_transaction: Transaction = Transaction(
    network=NETWORK, vapor=VAPOR
)
# Build Bytom transaction
unsigned_transaction.build_transaction(
    address=wallet.address(vapor=VAPOR),
    inputs=[
        spend_utxo(
            utxo=find_p2wsh_utxo(
                transaction_id="049d4c26bb15885572c16e0eefac5b2f4d0fde50eaf90f002272d39507ff315b",
                network=NETWORK
            )
        )
    ],
    outputs=[
        control_address(
            asset=ASSET,
            amount=10_000_000,
            address="bm1qwk4kpx09ehccrna3enqqwhrj9xt7pwxd4sufkw",
            symbol="NEU",
            vapor=VAPOR
        )
    ],
    fee=10_000_000,
    confirmations=1,
    forbid_chain_tx=False
)

print("Unsigned Transaction Fee:", unsigned_transaction.fee())
print("Unsigned Transaction Confirmations:", unsigned_transaction.confirmations())
print("Unsigned Transaction Hash:", unsigned_transaction.hash())
print("Unsigned Transaction Raw:", unsigned_transaction.raw())
# print("Unsigned Transaction Json:", json.dumps(unsigned_transaction.json(), indent=4))
print("Unsigned Transaction Unsigned Datas:",
      json.dumps(unsigned_transaction.unsigned_datas(detail=False), indent=4))
print("Unsigned Transaction Signatures:", json.dumps(unsigned_transaction.signatures(), indent=4))

# Sing unsigned transaction by xprivate key
signed_transaction: Transaction = unsigned_transaction.sign(
    xprivate_key=wallet.xprivate_key(), path=PATH
)

print("\nSigned Transaction Fee:", signed_transaction.fee())
print("Signed Transaction Confirmations:", signed_transaction.confirmations())
print("Signed Transaction Hash:", signed_transaction.hash())
print("Signed Transaction Raw:", signed_transaction.raw())
# print("Signed Transaction Json:", json.dumps(signed_transaction.json(), indent=4))
print("Signed Transaction Unsigned Datas:",
      json.dumps(signed_transaction.unsigned_datas(detail=False), indent=4))
print("Signed Transaction Signatures:", json.dumps(signed_transaction.signatures(), indent=4))

# Submit transaction raw
# print("\nSubmitted Transaction Id:", submit_transaction_raw(
#     address=wallet.address(vapor=VAPOR),
#     transaction_raw=signed_transaction.raw(),
#     signatures=signed_transaction.signatures(),
#     network=NETWORK,
#     vapor=VAPOR
# ))
