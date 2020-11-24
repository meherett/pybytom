#!/usr/bin/env python3

from typing import List

from .. config import config
from .wallet import Wallet
from .tools import (
    get_xpublic_key, get_expand_xprivate_key, get_child_xprivate_key, indexes_to_path,
    get_child_xpublic_key, get_address, get_program, get_private_key,
    get_public_key, get_bytes, path_to_indexes
)

# Bytom config
config: dict = config()

# Default derivation path
DEFAULT_PATH: str = config["path"]
# Default derivation indexes
DEFAULT_INDEXES: List[str] = config["indexes"]


__all__: List[str] = [
    "Wallet", "DEFAULT_PATH", "DEFAULT_INDEXES",
    "get_xpublic_key", "get_expand_xprivate_key", "get_child_xprivate_key",
    "get_child_xpublic_key", "get_address", "get_program",
    "get_private_key", "get_public_key", "get_bytes",
    "indexes_to_path", "path_to_indexes"
]
