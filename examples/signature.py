#!/usr/bin/env python3

from bytom import sign, verify

PRIVATE_KEY = "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee" \
              "0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"

PUBLIC_KEY = "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"

MESSAGE = "1246b84985e1ab5f83f4ec2bdf271114666fd3d9e24d12981a3c861b9ed523c6"

signed = sign(private=PRIVATE_KEY, message=MESSAGE)
print("Sign:", signed)
print("Verify:", verify(public=PUBLIC_KEY, message=MESSAGE, signature=signed))
