#!/usr/bin/env python3

import hashlib

from .utils import get_expanded_private_key, _verify, get_public_key, \
    sc_reduce32, decodeint, encodepoint, scalarmultbase, get_xpublic_key, sc_muladd


def sign(private_key, message):
    """
    Sign bytom message data by private key.

    :param private_key: Bytom private key.
    :type private_key: str.
    :param message: Message data.
    :type message: str.
    :return: str -- bytom signed message or signature.

    >>> from pybytom.signature import sign
    >>> sign(bytom_private_key, message_data)
    "..."
    """

    private = get_expanded_private_key(private_key)
    private_bytes = bytes.fromhex(private)
    message_bytes = bytes.fromhex(message)
    data_bytes = private_bytes[32:64] + message_bytes

    message_digest = hashlib.sha512(data_bytes).digest()
    message_digest = sc_reduce32(message_digest.hex().encode())
    message_digest = bytes.fromhex(message_digest.decode())
    message_digest_reduced = message_digest[0:32]

    scalar = decodeint(message_digest_reduced)
    encoded_r = encodepoint(scalarmultbase(scalar))
    public = get_xpublic_key(private)
    public_bytes = bytes.fromhex(public)
    hram_digest_data = encoded_r + public_bytes[:32] + message_bytes

    hram_digest = hashlib.sha512(hram_digest_data).digest()
    hram_digest = sc_reduce32(hram_digest.hex().encode())
    hram_digest = bytes.fromhex(hram_digest.decode())
    hram_digest_reduced = hram_digest[0:32]

    sk = private_bytes[:32]
    s = sc_muladd(hram_digest_reduced.hex().encode(), sk.hex().encode(), message_digest_reduced.hex().encode())
    s = bytes.fromhex(s.decode())

    signature_bytes = encoded_r + s
    signature = signature_bytes.hex()
    return signature


def verify(public_key, message, signature):
    """
    Verify bytom signature by public key.

    :param public_key: Bytom public key.
    :type public_key: str.
    :param message: Message data.
    :type message: str.
    :param signature: Signed message data.
    :type signature: str.
    :return: bool -- verified signature.

    >>> from pybytom.signature import verify
    >>> verify(bytom_private_key, message_data, bytom_signature)
    True
    """

    return _verify(get_public_key(public_key), signature, message)
