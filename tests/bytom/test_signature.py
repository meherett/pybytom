#!/usr/bin/env python3

from bytom.signature import sign, verify


PRIVATE_KEY = "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee" \
              "0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"

PUBLIC_KEY = "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"

MESSAGE = "1246b84985e1ab5f83f4ec2bdf271114666fd3d9e24d12981a3c861b9ed523c6"


def test_signature():

    signed = sign(private=PRIVATE_KEY, message=MESSAGE)

    assert signed == "f6624fea84fadccbc1bc72dc384f662468e271c4e32d846bc0a152447054999" \
                     "2c8ffcc3ca43891a30de4235392b0868c506ed254f0f77cc1f2b9c1a2385ddb05"

    assert verify(public=PUBLIC_KEY, message=MESSAGE, signature=signed)
