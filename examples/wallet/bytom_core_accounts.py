#!/usr/bin/env python3

from pybytom.wallet import Wallet
from pybytom.utils import generate_mnemonic, is_mnemonic

import json

# 12 word mnemonic seed
MNEMONIC = "병아리 실컷 여인 축제 극히 저녁 경찰 설사 할인 해물 시각 자가용"
# Or generate mnemonic
# MNEMONIC = generate_mnemonic(language="korean", strength=128)
# Secret passphrase
PASSPHRASE = None  # str("meherett")
# Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese & korean
LANGUAGE = "korean"  # default is english

# Checking 12 word mnemonic seed
assert is_mnemonic(mnemonic=MNEMONIC, language=LANGUAGE), \
      "Invalid %s 12 word mnemonic seed." % LANGUAGE

# Initialize wallet
wallet = Wallet(network="mainnet")
# Get Bytom wallet from mnemonic
wallet.from_mnemonic(mnemonic=MNEMONIC, passphrase=PASSPHRASE, language=LANGUAGE)

print("Mnemonic:", wallet.mnemonic())
print("XPrivate Key:", wallet.xprivate_key())
print("XPublic Key:", wallet.xpublic_key())
print("Base HD Path:  m/44/153/{ACCOUNT_INDEX}/{ADDRESSES_FOR_CHANGE}/{ADDRESS_INDEX}")

# Set address index
ADDRESS_INDEX = 1
# Set addresses for change
ADDRESSES_FOR_CHANGE = False
print("\nAddresses For Change:", ADDRESSES_FOR_CHANGE)
# Get wallet information's from account index
for account_index in range(10):
    # Derivation from path
    wallet.from_path(f"m/44/153/{account_index}/{1 if ADDRESSES_FOR_CHANGE else 0}/{ADDRESS_INDEX}")
    # Print account_index, change, addresses_index, address and private_key like bytom core wallet accounts
    print(f"({account_index}) ({ADDRESSES_FOR_CHANGE}) ({ADDRESS_INDEX}) {wallet.address()} {wallet.private_key()}")
    # Clean derivation
    wallet.clean_derivation()
