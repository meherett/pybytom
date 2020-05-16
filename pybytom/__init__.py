#!/usr/bin/env python3

from .wallet import Wallet
from .signature import sign, verify


# Bytom configuration
configuration = {
    "mainnet": {
        "bytom": "http://localhost:9888",
        "blockmeta": "https://blockmeta.com/api/v2",
        "blockcenter": "https://bcapi.bystack.com/api/v2/btm"
    },
    "solonet": {
        "bytom": "http://localhost:9888",
        "blockmeta": "https://blockmeta.com/api/v2",
        "blockcenter": "https://bcapi.bystack.com/api/v2/btm"
    },
    "testnet": {
        "bytom": "http://localhost:9888",
        "blockmeta": "https://blockmeta.com/api/wisdom",
        "blockcenter": "https://bcapi.bystack.com/api/v2/wisdom"
    },
    "timeout": 60,
    "BTM_asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    "fee": 10_000_000,
    "confirmations": 1,
    "sequence": 100
}

__all__ = [
    "configuration",
    "Wallet",
    "sign",
    "verify"
]
