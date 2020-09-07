#!/usr/bin/env python3


# Bytom configuration
def config():

    return {
        "mainnet": {
            "bytom": "http://localhost:9888",
            "blockmeta": "https://blockmeta.com/api/v3",
            "blockcenter": {
                "v2": "https://bcapi.bystack.com/api/v2/btm",
                "v3": "https://bcapi.bystack.com/bytom/v3"
            },
            "mov": "https://ex.movapi.com/bytom/v3"
        },
        "solonet": {
            "bytom": "http://localhost:9888",
            "blockmeta": None,
            "blockcenter": {
                "v2": None,
                "v3": None
            },
            "mov": None
        },
        "testnet": {
            "bytom": "http://localhost:9888",
            "blockmeta": None,
            "blockcenter": {
                "v2": None,
                "v3": None
            },
            "mov": None
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
        "confirmations": 1
    }
