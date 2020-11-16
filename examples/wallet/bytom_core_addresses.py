#!/usr/bin/env python3

from pybytom.wallet import Wallet
from pybytom.utils import (
    generate_mnemonic, is_mnemonic
)
from typing import Optional

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"  # Default is mainnet
# Choose strength 128, 160, 192, 224 or 256
STRENGTH: int = 128  # Default is 128
# Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
LANGUAGE: str = "english"  # Default is english
# Generate new mnemonic words
MNEMONIC: str = generate_mnemonic(language=LANGUAGE, strength=STRENGTH)
# Secret passphrase/password for mnemonic
PASSPHRASE: Optional[str] = None  # str("meherett")

# Check mnemonic words
assert is_mnemonic(mnemonic=MNEMONIC, language=LANGUAGE)

# Initialize Bytom wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Bytom wallet from mnemonic
wallet.from_mnemonic(
    mnemonic=MNEMONIC, passphrase=PASSPHRASE, language=LANGUAGE
)

print("Mnemonic:", wallet.mnemonic())
print("XPrivate Key:", wallet.xprivate_key())
print("XPublic Key:", wallet.xpublic_key())
print("Base HD Path:  m/44/153/{ACCOUNT_INDEX}/{CHANGE}/{ADDRESS_INDEX}")

# Set account index
ACCOUNT_INDEX = 1

# Set change
CHANGE = False
print("\nChange:", CHANGE)
# Get wallet information's from account index
for address_index in range(1, 10):
    # Derivation from path
    wallet.from_path(f"m/44/153/{ACCOUNT_INDEX}/{1 if CHANGE else 0}/{address_index}")
    # Print account_index, change, addresses_index, address and private_key like bytom core wallet accounts
    print(f"({ACCOUNT_INDEX}) ({CHANGE}) ({address_index}) {wallet.address()} {wallet.private_key()}")
    # Clean derivation
    wallet.clean_derivation()

# Set addresses for change
CHANGE = True
print("\nAddresses For Change:", CHANGE)
# Get wallet information's from account index
for address_index in range(1, 10):
    # Derivation from path
    wallet.from_path(f"m/44/153/{ACCOUNT_INDEX}/{1 if CHANGE else 0}/{address_index}")
    # Print account_index, change, addresses_index, address and private_key like bytom core wallet accounts
    print(f"({ACCOUNT_INDEX}) ({CHANGE}) ({address_index}) {wallet.address()} {wallet.private_key()}")
    # Clean derivation
    wallet.clean_derivation()
