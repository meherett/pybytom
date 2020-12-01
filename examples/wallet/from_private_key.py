#!/usr/bin/env python3

from pybytom.wallet import Wallet
from pybytom.assets import BTM as ASSET
from pybytom.utils import amount_converter

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"  # Default is mainnet
# Bytom private key
PRIVATE_KEY: str = "e0d42c3a1d9e1c54c09d5da9fd582afb1d053d3c033c3a07fedf2a709ce3f4477b4" \
                   "b52132f610150767edac6e1c2934d34780a9340a56a9dea58e070e44b70f1"
# Message data
MESSAGE: str = "a0841d35364046649ab8fc4af5a6266245890778f6cf7304696c4ab8edd86242"

# Initialize Bytom wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Bytom wallet private key
wallet.from_private_key(private_key=PRIVATE_KEY)

# Print all wallet information's
# print(json.dumps(wallet.dumps(), indent=4, ensure_ascii=False))

print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Program:", wallet.program())
print("Address:", wallet.address(vapor=False))
print("Vapor Address:", wallet.address(vapor=True))
print("Balance:", amount_converter(wallet.balance(asset=ASSET, vapor=False), "NEU2BTM"), "BTM")
print("Vapor Balance:", amount_converter(wallet.balance(asset=ASSET, vapor=True), "NEU2BTM"), "BTM")
print("UTXO's:", wallet.utxos(asset=ASSET, vapor=False))
print("Vapor UTXO's:", wallet.utxos(asset=ASSET, vapor=True))

print("-------- Sign & Verify --------")

print("Message:", MESSAGE)
signature = wallet.sign(message=MESSAGE)
print("Signature:", signature)
print("Verified:", wallet.verify(message=MESSAGE, signature=signature))
