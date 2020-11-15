#!/usr/bin/env python3

from struct import pack
from binascii import unhexlify
from ctypes import c_int64

from .opcode import (
    OP_0, OP_1, OP_DATA_1, OP_PUSHDATA1, OP_PUSHDATA2, OP_PUSHDATA4
)


class Builder:

    def __init__(self):
        self.program = bytearray()

    def add_op(self, op: int) -> "Builder":
        self.program.append(op)
        return self

    def add_bytes(self, data: bytes) -> "Builder":
        len_byte = len(data)

        if len_byte == 0:
            self.program.append(OP_0)
        elif len_byte <= 75:
            self.program.append(
                OP_DATA_1 + len_byte - 1
            )
            self.program += data
        elif len_byte < 1 << 8:
            self.program.append(OP_PUSHDATA1)
            self.program.append(len_byte)
            self.program += data
        elif len_byte < 1 << 16:
            self.program.append(OP_PUSHDATA2)
            self.program += pack("<H", len_byte)
            self.program += data
        else:
            self.program.append(OP_PUSHDATA4)
            self.program += pack("<L", len_byte)
            self.program += data
        return self

    def add_int(self, number: int) -> "Builder":
        if number == 0:
            self.program.append(OP_0)
            return self
        if 1 <= number <= 16:
            self.program.append(
                OP_1 + number - 1
            )
            return self
        # return
        return self.add_bytes(
            bytes(c_int64(number)).rstrip(b'\x00'))
    
    def add_raw_bytes(self, data: str) -> "Builder":
        self.program.append(
            unhexlify(data)
        )
        return self

    def digest(self) -> bytearray:
        return self.program

    def hex_digest(self) -> str:
        return self.program.hex()
