#!/usr/bin/env python3

from pybytom.wallet.tools import (
    path_to_indexes, indexes_to_path, get_xpublic_key, get_expand_xprivate_key,
    get_child_xprivate_key, get_child_xpublic_key, get_private_key,
    get_public_key, get_program, get_address
)


import pytest


XPRIVATE_KEY = "3842e3fa2af2a687e7fd67655e7a02e85bbb4ca378d4338ff590dedc7ddff447797e1e" \
               "781190835138c2d1a96d0e654b625a4c019cbc64f71100be7ad1b8d4ed"

XPUBLIC_KEY = "38a1bfcb82358bc9657c725d5d708c9d0ce115474466520e88fca233be2bc7e3797e1e7" \
              "81190835138c2d1a96d0e654b625a4c019cbc64f71100be7ad1b8d4ed"

INDEXES = ['2c000000', '99000000', '01000000', '00000000', '01000000']

PATH = "m/44/153/1/0/1"


def test_wallet_tools():
    assert get_xpublic_key(xprivate_key=XPRIVATE_KEY) == "38a1bfcb82358bc9657c725d5d708c9d0ce115474466520e88fca23" \
                                                         "3be2bc7e3797e1e781190835138c2d1a96d0e654b625a4c019cbc64" \
                                                         "f71100be7ad1b8d4ed"
    assert get_expand_xprivate_key(xprivate_key=XPRIVATE_KEY) == "3842e3fa2af2a687e7fd67655e7a02e85bbb4ca378d4338" \
                                                                 "ff590dedc7ddff447d51e53ef87283372fc866a4e0fb04e" \
                                                                 "b84487a872e30d546c4bf7c84388743631"

    assert indexes_to_path(indexes=INDEXES) == "m/44/153/1/0/1"
    assert path_to_indexes(path=PATH) == ['2c000000', '99000000', '01000000', '00000000', '01000000']

    assert get_child_xprivate_key(xprivate_key=XPRIVATE_KEY) == \
        "e0d42c3a1d9e1c54c09d5da9fd582afb1d053d3c033c3a07fedf2a709ce3f4477b4b52132f610150767edac6e1c2934d34780a93" \
        "40a56a9dea58e070e44b70f1"
    assert get_child_xprivate_key(xprivate_key=XPRIVATE_KEY, indexes=INDEXES) == \
        "e0d42c3a1d9e1c54c09d5da9fd582afb1d053d3c033c3a07fedf2a709ce3f4477b4b52132f610150767edac6e1c2934d34780a93" \
        "40a56a9dea58e070e44b70f1"
    assert get_child_xprivate_key(xprivate_key=XPRIVATE_KEY, path=PATH) == \
        "e0d42c3a1d9e1c54c09d5da9fd582afb1d053d3c033c3a07fedf2a709ce3f4477b4b52132f610150767edac6e1c2934d34780a93" \
        "40a56a9dea58e070e44b70f1"
    assert get_child_xpublic_key(xpublic_key=XPUBLIC_KEY) == \
        "aff7ee67f0721064ce0e53843f43eea7dcef0a9606bf796da8dc71fd035898547b4b52132f610150767edac6e1c2934d34780a93" \
        "40a56a9dea58e070e44b70f1"
    assert get_child_xpublic_key(xpublic_key=XPUBLIC_KEY, indexes=INDEXES) == \
        "aff7ee67f0721064ce0e53843f43eea7dcef0a9606bf796da8dc71fd035898547b4b52132f610150767edac6e1c2934d34780a93" \
        "40a56a9dea58e070e44b70f1"
    assert get_child_xpublic_key(xpublic_key=XPUBLIC_KEY, path=PATH) == \
        "aff7ee67f0721064ce0e53843f43eea7dcef0a9606bf796da8dc71fd035898547b4b52132f610150767edac6e1c2934d34780a93" \
        "40a56a9dea58e070e44b70f1"

    assert get_private_key(xprivate_key=XPRIVATE_KEY) == "e0d42c3a1d9e1c54c09d5da9fd582afb1d053d3c033c3a07fedf2a7" \
                                                         "09ce3f4477b4b52132f610150767edac6e1c2934d34780a9340a56a" \
                                                         "9dea58e070e44b70f1"
    assert get_public_key(xpublic_key=XPUBLIC_KEY) == \
           "aff7ee67f0721064ce0e53843f43eea7dcef0a9606bf796da8dc71fd03589854"

    assert get_program(public_key=get_public_key(xpublic_key=XPUBLIC_KEY)) == \
           "00140d1c979ce4ad13f47429409b59a3b7098faff16b"
    assert get_address(program=get_program(
        public_key=get_public_key(xpublic_key=XPUBLIC_KEY)), network="mainnet") == \
        "bm1qp5wf088y45flgapfgzd4ngahpx86luttv8d8a5"
    assert get_address(program=get_program(
        public_key=get_public_key(xpublic_key=XPUBLIC_KEY)), network="solonet") == \
        "sm1qp5wf088y45flgapfgzd4ngahpx86luttdk8xa6"
    assert get_address(program=get_program(
        public_key=get_public_key(xpublic_key=XPUBLIC_KEY)), network="testnet") == \
        "tm1qp5wf088y45flgapfgzd4ngahpx86luttg3vra9"


def test_wallet_errors():

    # get_xpublic_key
    with pytest.raises(TypeError, match="xprivate key must be string format"):
        get_xpublic_key(float())
    # get_expand_xprivate_key
    with pytest.raises(TypeError, match="xprivate key must be string format"):
        get_expand_xprivate_key(float())
    # indexes_to_path
    with pytest.raises(TypeError, match="indexes must be list format"):
        indexes_to_path(str())
    # path_to_indexes
    with pytest.raises(TypeError, match="path must be string format"):
        path_to_indexes(list())
    with pytest.raises(ValueError, match=r"bad path, insert like this type of path .*"):
        path_to_indexes("mm/")
    assert path_to_indexes("m/44'/0/0/9'")
    # get_child_xprivate_key
    with pytest.raises(TypeError, match="xprivate key must be string format"):
        get_child_xprivate_key(float())
    with pytest.raises(TypeError, match="indexes must be list format"):
        get_child_xprivate_key(str(), indexes=float(1231))
    with pytest.raises(TypeError, match="path must be string format"):
        get_child_xprivate_key(str(), path=bool())
    #         get_child_xpublic_key(float())
    with pytest.raises(TypeError, match="xpublic key must be string format"):
        get_child_xpublic_key(float())
    with pytest.raises(TypeError, match="indexes must be list format"):
        get_child_xpublic_key(str(), indexes=float(1231))
    with pytest.raises(TypeError, match="path must be string format"):
        get_child_xpublic_key(str(), path=bool())
    # get_program
    with pytest.raises(TypeError, match="public key must be string format"):
        get_program(int())
    # get_address
    with pytest.raises(TypeError, match="program must be string format"):
        get_address(int())
    with pytest.raises(TypeError, match="network must be string format"):
        get_address(str(), float())
    with pytest.raises(ValueError, match=r"invalid network option, .*"):
        get_address(str(), str())
