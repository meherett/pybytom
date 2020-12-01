#!/usr/bin/env python3

from pybytom.rpc import get_balance
from pybytom.utils import is_address, amount_converter
from pybytom.assets import BTM as ASSET

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"
# Pay to Witness Public Key Hash Address
P2WPKH_ADDRESS: str = "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
# Pay to Witness Script Hash Address
P2WSH_ADDRESS: str = "bm1qul37cmn85j9m0f8wxglsfsj3jyl8w4g8hdw8wjsh4g8eqhg925xqheeud2"
# Vapor Pay to Witness Public Key Hash Address
VAPOR_P2WPKH_ADDRESS: str = "vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag"
# Vapor Pay to Witness Script Hash Address
VAPOR_P2WSH_ADDRESS: str = "vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37"

# Check all addresses
assert is_address(address=P2WPKH_ADDRESS, network=NETWORK, vapor=False)
assert is_address(address=P2WSH_ADDRESS, network=NETWORK, vapor=False)
assert is_address(address=VAPOR_P2WPKH_ADDRESS, network=NETWORK, vapor=True)
assert is_address(address=VAPOR_P2WSH_ADDRESS, network=NETWORK, vapor=True)

# Get all address balances
print("P2WPKH Address Balance:", amount_converter(
    amount=get_balance(
        address=P2WPKH_ADDRESS, asset=ASSET, network=NETWORK, vapor=False
    ),
    symbol="NEU2BTM"
), "BTM")
print("P2WSH Address Balance:", amount_converter(
    amount=get_balance(
        address=P2WSH_ADDRESS, asset=ASSET, network=NETWORK, vapor=False
    ),
    symbol="NEU2BTM"
), "BTM")
print("Vapor P2WPKH Address Balance:", amount_converter(
    amount=get_balance(
        address=VAPOR_P2WPKH_ADDRESS, asset=ASSET, network=NETWORK, vapor=True
    ),
    symbol="NEU2BTM"
), "BTM")
print("Vapor P2WSH Address Balance:", amount_converter(
    amount=get_balance(
        address=VAPOR_P2WSH_ADDRESS, asset=ASSET, network=NETWORK, vapor=True
    ),
    symbol="NEU2BTM"
), "BTM")
