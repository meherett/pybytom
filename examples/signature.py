#!/usr/bin/env python3

from pybytom.signature import sign, verify

# Bytom private key
PRIVATE_KEY: str = "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee51580" \
                   "3ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
# Bytom public key
PUBLIC_KEY: str = "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
# Message data
MESSAGE: str = "1246b84985e1ab5f83f4ec2bdf271114666fd3d9e24d12981a3c861b9ed523c6"

# Sign message by private key
signature: str = sign(private_key=PRIVATE_KEY, message=MESSAGE)
print("Signature:", signature)
# Verify signature by public key
verified: bool = verify(public_key=PUBLIC_KEY, signature=signature, message=MESSAGE)
print("Verified:", verified)
