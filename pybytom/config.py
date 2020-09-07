#!/usr/bin/env python3


# Bytom configuration
def config():

    return {
        "mainnet": {
            "bytom": "http://localhost:9888",
            "blockmeta": "https://blockmeta.com/api/v3",
            "blockcenter": {
                "version2": "https://bcapi.bystack.com/api/v2/btm",
                "version3": "https://bcapi.bystack.com/bytom/v3"
            },
            "mov": "https://ex.movapi.com/bytom/v3"
        },
        "solonet": {
            "bytom": "http://localhost:9888",
            "blockmeta": None,
            "blockcenter": {
                "version2": None,
                "version3": None
            },
            "mov": None
        },
        "testnet": {
            "bytom": "http://localhost:9888",
            "blockmeta": None,
            "blockcenter": {
                "version2": None,
                "version3": None
            },
            "mov": None
        },
        "network": "mainnet",  # default network
        "timeout": 60,
        "BTM_asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "fee": 10_000_000,  # 0.1 BTM
        "confirmations": 1
    }
