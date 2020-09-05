#!/usr/bin/env python3


# Bytom configuration
def config():

    return {
        "mainnet": {
            "bytom": "http://localhost:9888",
            "blockmeta": "https://blockmeta.com/api/v3",
            "blockcenter": "https://bcapi.bystack.com/api/v3"
        },
        "solonet": {
            "bytom": "http://localhost:9888",
            "blockmeta": None,
            "blockcenter": None
        },
        "testnet": {
            "bytom": "http://localhost:9888",
            "blockmeta": None,
            "blockcenter": None
        },
        "network": "mainnet",  # default network
        "timeout": 60,
        "BTM_asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "one_BTM": 100_000_000,  # 1 BTM
        "fee": 10_000_000,  # 0.1 BTM
        "confirmations": 1
    }
