#!/usr/bin/env python3

from pybytom.wallet import Wallet, DEFAULT_PATH
from pybytom.assets import BTM as ASSET
from pybytom.transaction import AdvancedTransaction
from pybytom.transaction.actions import spend_utxo, control_address
from pybytom.transaction.tools import find_p2wsh_utxo
from pybytom.rpc import submit_transaction_raw, estimate_transaction_fee
from pybytom.utils import amount_converter

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"  # Default is mainnet
# Bytom sidechain (Vapor protocol)
VAPOR: bool = False  # Default is False
# Wallet mnemonic words
MNEMONIC: str = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"

# Initialize Bytom wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Bytom wallet from mnemonic
wallet.from_mnemonic(mnemonic=MNEMONIC)
# Derivation from path
wallet.from_path(path=DEFAULT_PATH)

# Initialize Bytom advanced transaction
unsigned_advanced_transaction: AdvancedTransaction = AdvancedTransaction(
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

# Build Bytom advanced transaction
unsigned_advanced_transaction.build_transaction(
    wallet.address(vapor=VAPOR),  # address
    [
        spend_utxo(
            utxo=find_p2wsh_utxo(
                transaction_id="049d4c26bb15885572c16e0eefac5b2f4d0fde50eaf90f002272d39507ff315b",
                network=NETWORK,
                vapor=VAPOR
            )
        )
    ],  # inputs
    [
        control_address(
            asset=ASSET,
            amount=0.0001,
            address=wallet.address(vapor=VAPOR),
            symbol="BTM"
        )
    ],  # outputs
    estimated_transaction_fee,  # fee
    1,  # confirmations
    False,  # forbid_chain_tx
)

print("\nUnsigned Advanced Transaction Fee:", unsigned_advanced_transaction.fee())
print("Unsigned Advanced Transaction Confirmations:", unsigned_advanced_transaction.confirmations())
print("Unsigned Advanced Transaction Hash:", unsigned_advanced_transaction.hash())
print("Unsigned Advanced Transaction Raw:", unsigned_advanced_transaction.raw())
# print("Unsigned Advanced Transaction Json:", json.dumps(unsigned_advanced_transaction.json(), indent=4))
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
#     address=wallet.address(vapor=VAPOR),
#     transaction_raw=signed_advanced_transaction.raw(),
#     signatures=signed_advanced_transaction.signatures(),
#     network=NETWORK,
#     vapor=VAPOR
# ))
