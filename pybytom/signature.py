#!/usr/bin/env python3

import hashlib
import ed25519
import hmac

from .wallet.tools import get_xpublic_key
from .libs.ed25519 import (
    sc_reduce32, decodeint, scalarmultbase, encodepoint, sc_muladd
)


def sign(private_key: str, message: str) -> str:
    """
    Sign Bytom message data by private key.

    :param private_key: Bytom private key.
    :type private_key: str.
    :param message: Message data.
    :type message: str.
    :return: str -- Bytom signed message or signature.

    >>> from pybytom.signature import sign
    >>> sign(private_key="e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141", message="1246b84985e1ab5f83f4ec2bdf271114666fd3d9e24d12981a3c861b9ed523c6")
    "f6624fea84fadccbc1bc72dc384f662468e271c4e32d846bc0a1524470549992c8ffcc3ca43891a30de4235392b0868c506ed254f0f77cc1f2b9c1a2385ddb05"
    """

    hc_hexstr = hmac.HMAC(
        b"Expand", bytes.fromhex(private_key),
        digestmod=hashlib.sha512).hexdigest()
    private = private_key[:64] + hc_hexstr[64:]
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
    hram_digest_data = (
        encoded_r + public_bytes[:32] + message_bytes
    )
    hram_digest = hashlib.sha512(hram_digest_data).digest()
    hram_digest = sc_reduce32(hram_digest.hex().encode())
    hram_digest = bytes.fromhex(hram_digest.decode())
    hram_digest_reduced = hram_digest[0:32]

    sk = private_bytes[:32]
    s = sc_muladd(hram_digest_reduced.hex().encode(),
                  sk.hex().encode(), message_digest_reduced.hex().encode())
    s = bytes.fromhex(s.decode())

    signature_bytes = encoded_r + s
    signature = signature_bytes.hex()
    return signature


def verify(public_key: str, message: str, signature: str) -> bool:
    """
    Verify Bytom signature by public key.

    :param public_key: Bytom public key.
    :type public_key: str.
    :param message: Message data.
    :type message: str.
    :param signature: Signed message data.
    :type signature: str.
    :return: bool -- verified signature.

    >>> from pybytom.signature import verify
    >>> verify(public_key="91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", message="1246b84985e1ab5f83f4ec2bdf271114666fd3d9e24d12981a3c861b9ed523c6", signature="f6624fea84fadccbc1bc72dc384f662468e271c4e32d846bc0a1524470549992c8ffcc3ca43891a30de4235392b0868c506ed254f0f77cc1f2b9c1a2385ddb05")
    True
    """

    result = False
    verifying_key = ed25519.VerifyingKey(
        public_key.encode(), encoding="hex"
    )
    try:
        verifying_key.verify(
            signature.encode(),
            bytes.fromhex(message), encoding="hex"
        )
        result = True
    except ed25519.BadSignatureError:
        result = False
    return result
