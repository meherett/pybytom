#!/usr/bin/env python3

from pybytom.script import (
    script_hash, p2sh_program, p2wsh_program, p2wsh_address
)


bytecode = "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a64175418" \
           "2d53f0677cd4351a0e743e6f10b35122c3d7ea01203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e" \
           "9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"


def test_p2ws():

    assert script_hash(bytecode=bytecode) == "e7e3ec6e67a48bb7a4ee323f04c251913e775507bb5c774a17aa0f905d05550c"

    assert p2sh_program(script_hash=script_hash(bytecode=bytecode)) == \
        "76aa20e7e3ec6e67a48bb7a4ee323f04c251913e775507bb5c774a17aa0f905d05550c8808ffffffffffffffff7c00c0"

    assert p2wsh_program(script_hash=script_hash(bytecode=bytecode)) == \
        "0020e7e3ec6e67a48bb7a4ee323f04c251913e775507bb5c774a17aa0f905d05550c"

    assert p2wsh_address(script_hash=script_hash(bytecode=bytecode), network="mainnet") == \
        "bm1qul37cmn85j9m0f8wxglsfsj3jyl8w4g8hdw8wjsh4g8eqhg925xqheeud2"

