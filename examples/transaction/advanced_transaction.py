#!/usr/bin/env python3

from pybytom.wallet import Wallet
from pybytom.assets import BTM as ASSET
from pybytom.transaction import AdvancedTransaction
from pybytom.transaction.tools import find_p2wsh_utxo
from pybytom.transaction.actions import (
    spend_utxo, control_address
)
from pybytom.rpc import submit_transaction_raw
from typing import Optional

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"
# Bytom sidechain vapor
VAPOR: bool = False
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

# Initialize Bytom advanced transaction
unsigned_advanced_transaction: AdvancedTransaction = AdvancedTransaction(
    network=NETWORK, vapor=VAPOR
)
# Build Bytom advanced transaction
unsigned_advanced_transaction.build_transaction(
    wallet.address(),  # address
    [
        spend_utxo(
            utxo=find_p2wsh_utxo(
                transaction_id="049d4c26bb15885572c16e0eefac5b2f4d0fde50eaf90f002272d39507ff315b",
                network=NETWORK
            )
        )
    ],  # inputs
    [
        control_address(
            asset=ASSET,
            amount=0.1,
            address="bm1qwk4kpx09ehccrna3enqqwhrj9xt7pwxd4sufkw",
            symbol="BTM"
        )
    ],  # outputs
    10_000_000,  # fee
    1,  # confirmations
    False,  # forbid_chain_tx
)

print("Unsigned Advanced Transaction Fee:", unsigned_advanced_transaction.fee())
print("Unsigned Advanced Transaction Confirmations:", unsigned_advanced_transaction.confirmations())
print("Unsigned Advanced Transaction Hash:", unsigned_advanced_transaction.hash())
print("Unsigned Advanced Transaction Raw:", unsigned_advanced_transaction.raw())
print("Unsigned Advanced Transaction Json:", json.dumps(unsigned_advanced_transaction.json(), indent=4))
print("Unsigned Advanced Transaction Unsigned Datas:",
      json.dumps(unsigned_advanced_transaction.unsigned_datas(detail=False), indent=4))
print("Unsigned Advanced Transaction Signatures:", json.dumps(unsigned_advanced_transaction.signatures(), indent=4))

# Sing unsigned advanced transaction by xprivate key
signed_advanced_transaction: AdvancedTransaction = unsigned_advanced_transaction.sign(
    xprivate_key=wallet.xprivate_key(), account=1, change=False, address=1
)

print("\nSigned Advanced Transaction Fee:", signed_advanced_transaction.fee())
print("Signed Advanced Transaction Confirmations:", signed_advanced_transaction.confirmations())
print("Signed Advanced Transaction Hash:", signed_advanced_transaction.hash())
print("Signed Advanced Transaction Raw:", signed_advanced_transaction.raw())
print("Signed Advanced Transaction Json:", json.dumps(signed_advanced_transaction.json(), indent=4))
print("Signed Advanced Transaction Unsigned Datas:",
      json.dumps(signed_advanced_transaction.unsigned_datas(detail=False), indent=4))
print("Signed Advanced Transaction Signatures:", json.dumps(signed_advanced_transaction.signatures(), indent=4))

# Submit advanced transaction raw
# print("\nSubmitted Advanced Transaction Id:", submit_transaction_raw(
#     address=wallet.address(),
#     transaction_raw=signed_advanced_transaction.raw(),
#     signatures=signed_advanced_transaction.signatures(),
#     network=NETWORK,
#     vapor=VAPOR
# ))
