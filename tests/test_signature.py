#!/usr/bin/env python3

import hashlib
import json
import os

from pybytom.signature import sign, verify

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()

MESSAGE: str = hashlib.sha256("meherett".encode()).hexdigest()


def test_signature():

    signature = sign(private_key=_["wallet"]["private_key"], message=MESSAGE)
    assert isinstance(signature, str)
    assert verify(public_key=_["wallet"]["public_key"], message=MESSAGE, signature=signature)
