#!/usr/bin/env python3

from typing import List

OP_FALSE: int = 0x00
OP_TRUE: int = 0x51

OP_0: int = 0x00
OP_1: int = 0x51
OP_2: int = 0x52
OP_3: int = 0x53
OP_4: int = 0x54
OP_5: int = 0x55
OP_6: int = 0x56
OP_7: int = 0x57
OP_8: int = 0x58
OP_9: int = 0x59
OP_10: int = 0x5a
OP_11: int = 0x5b
OP_12: int = 0x5c
OP_13: int = 0x5d
OP_14: int = 0x5e
OP_15: int = 0x5f
OP_16: int = 0x60

OP_DATA_1: int = 0x01
OP_DATA_2: int = 0x02
OP_DATA_3: int = 0x03
OP_DATA_4: int = 0x04
OP_DATA_5: int = 0x05
OP_DATA_6: int = 0x06
OP_DATA_7: int = 0x07
OP_DATA_8: int = 0x08
OP_DATA_9: int = 0x09
OP_DATA_10: int = 0x0a
OP_DATA_11: int = 0x0b
OP_DATA_12: int = 0x0c
OP_DATA_13: int = 0x0d
OP_DATA_14: int = 0x0e
OP_DATA_15: int = 0x0f
OP_DATA_16: int = 0x10
OP_DATA_17: int = 0x11
OP_DATA_18: int = 0x12
OP_DATA_19: int = 0x13
OP_DATA_20: int = 0x14
OP_DATA_21: int = 0x15
OP_DATA_22: int = 0x16
OP_DATA_23: int = 0x17
OP_DATA_24: int = 0x18
OP_DATA_25: int = 0x19
OP_DATA_26: int = 0x1a
OP_DATA_27: int = 0x1b
OP_DATA_28: int = 0x1c
OP_DATA_29: int = 0x1d
OP_DATA_30: int = 0x1e
OP_DATA_31: int = 0x1f
OP_DATA_32: int = 0x20
OP_DATA_33: int = 0x21
OP_DATA_34: int = 0x22
OP_DATA_35: int = 0x23
OP_DATA_36: int = 0x24
OP_DATA_37: int = 0x25
OP_DATA_38: int = 0x26
OP_DATA_39: int = 0x27
OP_DATA_40: int = 0x28
OP_DATA_41: int = 0x29
OP_DATA_42: int = 0x2a
OP_DATA_43: int = 0x2b
OP_DATA_44: int = 0x2c
OP_DATA_45: int = 0x2d
OP_DATA_46: int = 0x2e
OP_DATA_47: int = 0x2f
OP_DATA_48: int = 0x30
OP_DATA_49: int = 0x31
OP_DATA_50: int = 0x32
OP_DATA_51: int = 0x33
OP_DATA_52: int = 0x34
OP_DATA_53: int = 0x35
OP_DATA_54: int = 0x36
OP_DATA_55: int = 0x37
OP_DATA_56: int = 0x38
OP_DATA_57: int = 0x39
OP_DATA_58: int = 0x3a
OP_DATA_59: int = 0x3b
OP_DATA_60: int = 0x3c
OP_DATA_61: int = 0x3d
OP_DATA_62: int = 0x3e
OP_DATA_63: int = 0x3f
OP_DATA_64: int = 0x40
OP_DATA_65: int = 0x41
OP_DATA_66: int = 0x42
OP_DATA_67: int = 0x43
OP_DATA_68: int = 0x44
OP_DATA_69: int = 0x45
OP_DATA_70: int = 0x46
OP_DATA_71: int = 0x47
OP_DATA_72: int = 0x48
OP_DATA_73: int = 0x49
OP_DATA_74: int = 0x4a
OP_DATA_75: int = 0x4b

OP_PUSHDATA1: int = 0x4c
OP_PUSHDATA2: int = 0x4d
OP_PUSHDATA4: int = 0x4e
OP_1NEGATE: int = 0x4f
OP_NOP: int = 0x61

OP_JUMP: int = 0x63
OP_JUMPIF: int = 0x64
OP_VERIFY: int = 0x69
OP_FAIL: int = 0x6a
OP_CHECKPREDICATE: int = 0xc0

OP_TOALTSTACK: int = 0x6b
OP_FROMALTSTACK: int = 0x6c
OP_2DROP: int = 0x6d
OP_2DUP: int = 0x6e
OP_3DUP: int = 0x6f
OP_2OVER: int = 0x70
OP_2ROT: int = 0x71
OP_2SWAP: int = 0x72
OP_IFDUP: int = 0x73
OP_DEPTH: int = 0x74
OP_DROP: int = 0x75
OP_DUP: int = 0x76
OP_NIP: int = 0x77
OP_OVER: int = 0x78
OP_PICK: int = 0x79
OP_ROLL: int = 0x7a
OP_ROT: int = 0x7b
OP_SWAP: int = 0x7c
OP_TUCK: int = 0x7d

OP_CAT: int = 0x7e
OP_SUBSTR: int = 0x7f
OP_LEFT: int = 0x80
OP_RIGHT: int = 0x81
OP_SIZE: int = 0x82
OP_CATPUSHDATA: int = 0x89

OP_INVERT: int = 0x83
OP_AND: int = 0x84
OP_OR: int = 0x85
OP_XOR: int = 0x86
OP_EQUAL: int = 0x87
OP_EQUALVERIFY: int = 0x88

OP_1ADD: int = 0x8b
OP_1SUB: int = 0x8c
OP_2MUL: int = 0x8d
OP_2DIV: int = 0x8e
OP_NEGATE: int = 0x8f
OP_ABS: int = 0x90
OP_NOT: int = 0x91
OP_0NOTEQUAL: int = 0x92
OP_ADD: int = 0x93
OP_SUB: int = 0x94
OP_MUL: int = 0x95
OP_DIV: int = 0x96
OP_MOD: int = 0x97
OP_LSHIFT: int = 0x98
OP_RSHIFT: int = 0x99
OP_BOOLAND: int = 0x9a
OP_BOOLOR: int = 0x9b
OP_NUMEQUAL: int = 0x9c
OP_NUMEQUALVERIFY: int = 0x9d
OP_NUMNOTEQUAL: int = 0x9e
OP_LESSTHAN: int = 0x9f
OP_GREATERTHAN: int = 0xa0
OP_LESSTHANOREQUAL: int = 0xa1
OP_GREATERTHANOREQUAL: int = 0xa2
OP_MIN: int = 0xa3
OP_MAX: int = 0xa4
OP_WITHIN: int = 0xa5

OP_SHA256: int = 0xa8
OP_SHA3: int = 0xaa
OP_HASH160: int = 0xab
OP_CHECKSIG: int = 0xac
OP_CHECKMULTISIG: int = 0xad
OP_TXSIGHASH: int = 0xae

OP_CHECKOUTPUT: int = 0xc1
OP_ASSET: int = 0xc2
OP_AMOUNT: int = 0xc3
OP_PROGRAM: int = 0xc4
OP_INDEX: int = 0xc9
OP_ENTRYID: int = 0xca
OP_OUTPUTID: int = 0xcb
OP_BLOCKHEIGHT: int = 0xcd


# OP_DATAS
def op_datas() -> List[int]:
    return [
        0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d,
        0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a,
        0x1b, 0x1c, 0x1d, 0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
        0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34,
        0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d, 0x3e, 0x3f, 0x40, 0x41,
        0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4a, 0x4b
    ]
