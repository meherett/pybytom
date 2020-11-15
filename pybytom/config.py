#!/usr/bin/env python3


# Bytom and Vapor configuration
def config():
    return {
        "bytom": {
            "mainnet": {
                "bytom": "http://localhost:9888",
                "blockmeta": "https://blockmeta.com/api/v3",
                "blockcenter": "https://bcapi.bystack.com/bytom/v3",
                "mov": "https://ex.movapi.com/bytom/v3"
            },
            "solonet": {
                "bytom": "http://localhost:9888",
                "blockmeta": None,
                "blockcenter": None,
                "mov": None
            },
            "testnet": {
                "bytom": "http://localhost:9888",
                "blockmeta": None,
                "blockcenter": None,
                "mov": None
            }
        },
        "vapor": {
            "mainnet": {
                "bytom": "http://localhost:9888",
                "blockmeta": "https://vapor.blockmeta.com/api/v1",
                "blockcenter": "https://ex.movapi.com/vapor/v3",
                "mov": "https://ex.movapi.com/bytom/v3"
            },
            "solonet": {
                "bytom": "http://localhost:9888",
                "blockmeta": None,
                "blockcenter": None,
                "mov": None
            },
            "testnet": {
                "bytom": "http://localhost:9888",
                "blockmeta": None,
                "blockcenter": None,
                "mov": None
            }
        },
        "network": "mainnet",
        "timeout": 60,
        "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "symbols": {
            "BTM": 1,
            "mBTM": 1000,
            "NEU": 100_000_000
        },
        "fee": 10_000_000,
        "confirmations": 1,
        "forbid_chain_tx": False,
        "headers": {
            "User-Agent": "PyBytom User Agent v0.1.0",
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json"
        }
    }
