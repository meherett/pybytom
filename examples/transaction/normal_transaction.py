#!/usr/bin/env python3

from pybytom.wallet import Wallet
from pybytom.transaction import NormalTransaction
from pybytom.assets import BTM as ASSET
from pybytom.utils import amount_converter
from pybytom.rpc import submit_transaction_raw
from typing import Optional

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"  # Default is mainnet
# Bytom sidechain (Vapor protocol)
VAPOR: bool = True  # Default is False
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

# Initialize normal transaction
unsigned_normal_transaction: NormalTransaction = NormalTransaction(
    network=NETWORK, vapor=VAPOR
)
# Build normal transaction
unsigned_normal_transaction.build_transaction(
    address=wallet.address(vapor=VAPOR),
    recipients={
        "vp1qzhm2ydkxcs242z2v6eca73zqrvjzw60gl0pt0w": amount_converter(0.01, "BTM2NEU")
    },
    asset=ASSET
)

print("Unsigned Normal Transaction Fee:", unsigned_normal_transaction.fee())
print("Unsigned Normal Transaction Confirmations:", unsigned_normal_transaction.confirmations())
print("Unsigned Normal Transaction Hash:", unsigned_normal_transaction.hash())
print("Unsigned Normal Transaction Raw:", unsigned_normal_transaction.raw())
print("Unsigned Normal Transaction Json:", json.dumps(unsigned_normal_transaction.json(), indent=4))
print("Unsigned Normal Transaction Unsigned Datas:",
      json.dumps(unsigned_normal_transaction.unsigned_datas(detail=False), indent=4))
print("Unsigned Normal Transaction Signatures:", json.dumps(unsigned_normal_transaction.signatures(), indent=4))

# Sing unsigned normal transaction by xprivate key
signed_normal_transaction: NormalTransaction = unsigned_normal_transaction.sign(
    xprivate_key=wallet.xprivate_key(), path=PATH
)

print("\nSigned Normal Transaction Fee:", signed_normal_transaction.fee())
print("Signed Normal Transaction Confirmations:", signed_normal_transaction.confirmations())
print("Signed Normal Transaction Hash:", signed_normal_transaction.hash())
print("Signed Normal Transaction Raw:", signed_normal_transaction.raw())
print("Signed Normal Transaction Json:", json.dumps(signed_normal_transaction.json(), indent=4))
print("Signed Normal Transaction Unsigned Datas:",
      json.dumps(signed_normal_transaction.unsigned_datas(detail=False), indent=4))
print("Signed Normal Transaction Signatures:", json.dumps(signed_normal_transaction.signatures(), indent=4))

# Submit normal transaction raw
# print("\nSubmitted Normal Transaction Id:", submit_transaction_raw(
#     address=wallet.address(vapor=VAPOR),
#     transaction_raw=signed_normal_transaction.raw(),
#     signatures=signed_normal_transaction.signatures(),
#     network=NETWORK,
#     vapor=VAPOR
# ))
