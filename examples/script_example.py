#!/usr/bin/env python3

from pybytom.script import (
    get_public_key_hash, get_script_hash,  # -> Hash
    get_p2wpkh_program, get_p2wsh_program,  # -> Program
    get_p2wpkh_address, get_p2wsh_address  # -> Address
)

# P2WPK
public_key = "5b5a06f6fbcb74b58ebb42293808fec6222234df6c97d7c1cff6d857a6024dc2"
print("Public Key:", public_key)
public_key_hash = get_public_key_hash(public_key=public_key)
print("Public Key Hash:", public_key_hash)
p2wpkh_program = get_p2wpkh_program(public_key_hash=public_key_hash)
print("P2WPKH Program:", p2wpkh_program)
p2wpkh_address = get_p2wpkh_address(public_key_hash=public_key_hash, network="mainnet")
print("P2WPKH Address:", p2wpkh_address)

# P2WS
bytecode = "7baa8800c3c251547ac1"  # Contract program
print("\nBytecode:", bytecode)
script_hash = get_script_hash(bytecode=bytecode)  # SHA3_256
print("Script Hash:", script_hash)
p2wsh_program = get_p2wsh_program(script_hash=script_hash)
print("P2WSH Program:", p2wsh_program)
p2wsh_address = get_p2wsh_address(script_hash=script_hash, network="mainnet")
print("P2WSH Address:", p2wsh_address)
