#!/usr/bin/env python3

from pybytom.wallet import Wallet, DEFAULT_BIP44
from pybytom.assets import BTM as ASSET
from pybytom.transaction import Transaction
from pybytom.transaction.actions import spend_utxo, control_address
from pybytom.transaction.tools import find_p2wsh_utxo
from pybytom.rpc import submit_transaction_raw, estimate_transaction_fee
from pybytom.utils import amount_converter

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"  # Default is mainnet
# Bytom sidechain (Vapor protocol)
VAPOR: bool = True  # Default is False
# Wallet mnemonic words
MNEMONIC: str = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"

# Initialize Bytom wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Bytom wallet from mnemonic
wallet.from_mnemonic(mnemonic=MNEMONIC)
# Derivation from path
wallet.from_path(
    path=DEFAULT_BIP44.format(
        account=1, change=0, address=1
    )
)

# Initialize Bytom transaction
unsigned_transaction: Transaction = Transaction(
    network=NETWORK, vapor=VAPOR
)

# Estimate transaction fee (returned NEU amount)
estimated_transaction_fee: int = estimate_transaction_fee(
    address=wallet.address(vapor=VAPOR),
    asset=ASSET,
    amount=amount_converter(0.0001, "BTM2NEU"),
    confirmations=1,
    network=NETWORK,
    vapor=VAPOR
)

print("Estimated Transaction Fee:", estimated_transaction_fee)

# Build Bytom transaction
unsigned_transaction.build_transaction(
    address=wallet.address(vapor=VAPOR),
    inputs=[
        spend_utxo(
            utxo=find_p2wsh_utxo(
                transaction_id="675392fcbc1867e247add457597611717229e5d2c46a53c44e3e61d6ce351474",
                network=NETWORK,
                vapor=VAPOR
            )
        )
    ],
    outputs=[
        control_address(
            asset=ASSET,
            amount=amount_converter(0.0001, "BTM2NEU"),
            address=wallet.address(vapor=VAPOR),
            symbol="NEU",
            vapor=VAPOR
        )
    ],
    fee=estimated_transaction_fee,
    confirmations=1
)

print("\nUnsigned Transaction Fee:", unsigned_transaction.fee())
print("Unsigned Transaction Confirmations:", unsigned_transaction.confirmations())
print("Unsigned Transaction Hash:", unsigned_transaction.hash())
print("Unsigned Transaction Raw:", unsigned_transaction.raw())
# print("Unsigned Transaction Json:", json.dumps(unsigned_transaction.json(), indent=4))
print("Unsigned Transaction Unsigned Datas:",
      json.dumps(unsigned_transaction.unsigned_datas(detail=False), indent=4))
print("Unsigned Transaction Signatures:", json.dumps(unsigned_transaction.signatures(), indent=4))

# Sing unsigned transaction by xprivate key
signed_transaction: Transaction = unsigned_transaction.sign(
    xprivate_key=wallet.xprivate_key(), path=wallet.path()
)

print("\nSigned Transaction Fee:", signed_transaction.fee())
print("Signed Transaction Confirmations:", signed_transaction.confirmations())
print("Signed Transaction Hash:", signed_transaction.hash())
print("Signed Transaction Raw:", signed_transaction.raw())
print("Signed Transaction Json:", json.dumps(signed_transaction.json(), indent=4))
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
