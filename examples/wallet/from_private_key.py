#!/usr/bin/env python3

from pybytom.wallet import Wallet

import json

# Bytom xprivate key
PRIVATE_KEY = "e0d42c3a1d9e1c54c09d5da9fd582afb1d053d3c033c3a07fedf2a709ce3f4477b4" \
              "b52132f610150767edac6e1c2934d34780a9340a56a9dea58e070e44b70f1"

# Message data
MESSAGE = "a0841d35364046649ab8fc4af5a6266245890778f6cf7304696c4ab8edd86242"

# Initialize wallet
wallet = Wallet(network="mainnet")
# Get Bytom wallet xprivate key
wallet.from_private_key(private_key=PRIVATE_KEY)

# Print all wallet information's
# print(json.dumps(wallet.dumps(), indent=4))

print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Program:", wallet.program())
print("Address:", wallet.address())
print("Vapor Address:", wallet.vapor_address())
# print("Balance:", wallet.balance())

print("-------- Sign & Verify --------")

print("Message:", MESSAGE)
signature = wallet.sign(message=MESSAGE)
print("Signature:", signature)
print("Verified:", wallet.verify(message=MESSAGE, signature=signature))