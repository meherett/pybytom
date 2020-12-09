#!/usr/bin/env python3

from pybytom.wallet import Wallet, DEFAULT_INDEXES
from pybytom.transaction import NormalTransaction
from pybytom.assets import BTM as ASSET
from pybytom.utils import amount_converter
from pybytom.rpc import submit_transaction_raw, estimate_transaction_fee

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"  # Default is mainnet
# Bytom sidechain (Vapor protocol)
VAPOR: bool = True  # Default is False
# Wallet entropy hex string
ENTROPY: str = "72fee73846f2d1a5807dc8c953bf79f1"

# Initialize Bytom wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Bytom wallet from mnemonic
wallet.from_entropy(entropy=ENTROPY)
# Derivation from default indexes
wallet.from_indexes(indexes=DEFAULT_INDEXES)

# Initialize normal transaction
unsigned_normal_transaction: NormalTransaction = NormalTransaction(
    network=NETWORK, vapor=VAPOR
)

# Estimate transaction fee (returned NEU amount)
estimated_transaction_fee: int = estimate_transaction_fee(
    address=wallet.address(vapor=VAPOR),
    asset=ASSET,
    amount=amount_converter(0.1, "BTM2NEU"),
    confirmations=1,
    network=NETWORK,
    vapor=VAPOR
)

print("Estimated Transaction Fee:", estimated_transaction_fee)

# Build normal transaction
unsigned_normal_transaction.build_transaction(
    address=wallet.address(vapor=VAPOR),
    recipients={
        "vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag": amount_converter(0.1, "BTM2NEU")
    },
    asset=ASSET,
    fee=estimated_transaction_fee,
    confirmations=1
)

print("\nUnsigned Normal Transaction Fee:", unsigned_normal_transaction.fee())
print("Unsigned Normal Transaction Confirmations:", unsigned_normal_transaction.confirmations())
print("Unsigned Normal Transaction Hash:", unsigned_normal_transaction.hash())
print("Unsigned Normal Transaction Raw:", unsigned_normal_transaction.raw())
# print("Unsigned Normal Transaction Json:", json.dumps(unsigned_normal_transaction.json(), indent=4))
print("Unsigned Normal Transaction Unsigned Datas:",
      json.dumps(unsigned_normal_transaction.unsigned_datas(detail=False), indent=4))
print("Unsigned Normal Transaction Signatures:", json.dumps(unsigned_normal_transaction.signatures(), indent=4))

# Sing unsigned normal transaction by xprivate key
signed_normal_transaction: NormalTransaction = unsigned_normal_transaction.sign(
    xprivate_key=wallet.xprivate_key(), indexes=DEFAULT_INDEXES
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
