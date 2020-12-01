#!/usr/bin/env python3

from .assets import BTM as ASSET


# Bytom mainchain & sidechain configuration
config: dict = {
    "mainchain": {
        "mainnet": {
            "bytom-core": "http://localhost:9888",
            "blockmeta": "https://blockmeta.com/api/v3",
            "blockcenter": "https://bcapi.bystack.com/bytom/v3",
            "mov": "https://ex.movapi.com/bytom/v3"
        },
        "solonet": {
            "bytom-core": "http://localhost:9888",
            "blockmeta": None,
            "blockcenter": None,
            "mov": None
        },
        "testnet": {
            "bytom-core": "http://localhost:9888",
            "blockmeta": None,
            "blockcenter": None,
            "mov": None
        }
    },
    "sidechain": {
        "mainnet": {
            "vapor-core": "http://localhost:9889",
            "blockmeta": "https://vapor.blockmeta.com/api/v1",
            "blockcenter": "https://bcapi.bystack.com/vapor/v3",
            "mov": "https://ex.movapi.com/vapor/v3"
        },
        "solonet": {
            "vapor-core": "http://localhost:9889",
            "blockmeta": None,
            "blockcenter": None,
            "mov": None
        },
        "testnet": {
            "vapor-core": "http://localhost:9889",
            "blockmeta": None,
            "blockcenter": None,
            "mov": None
        }
    },
    "harden": 0x80000000,
    "vapor": False,
    "network": "mainnet",
    "timeout": 60,
    "asset": ASSET,
    "symbols": {
        "BTM": 1,
        "mBTM": 1000,
        "NEU": 100_000_000
    },
    "path": "m/44/153/1/0/1",
    "BIP44": "m/44/153/{account}/{change}/{address}",
    "indexes": ["2c000000", "99000000", "01000000", "00000000", "01000000"],
    "fee": 10_000_000,
    "confirmations": 1,
    "forbid_chain_tx": False,
    "headers": {
        "User-Agent": "PyBytom User Agent v0.1.0",
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json"
    }
}
