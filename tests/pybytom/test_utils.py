#!/usr/bin/env python3

from pybytom.utils import generate_mnemonic, generate_entropy, is_mnemonic, get_mnemonic_language

import pytest


MNEMONIC = "병아리 실컷 여인 축제 극히 저녁 경찰 설사 할인 해물 시각 자가용"


def test_base58():

    assert len(generate_entropy(strength=128)) == 32

    assert len(generate_mnemonic(language="chinese_traditional", strength=128).split(" ")) == 12

    with pytest.raises(ValueError, match=r".*[128, 160, 192, 224, 256].*"):
        assert len(generate_entropy(strength=129).split(" ")) == 12

    assert is_mnemonic(mnemonic=MNEMONIC, language="korean")

    with pytest.raises(ValueError, match=r"invalid language, .*"):
        assert is_mnemonic(mnemonic=MNEMONIC, language="amharic")

    assert not is_mnemonic(mnemonic=12341234, language="english")

    with pytest.raises(ValueError, match="invalid 12 word mnemonic."):
        assert get_mnemonic_language("1234 meheret tesfaye")

    with pytest.raises(ValueError, match=r"invalid language, .*"):
        assert generate_mnemonic(language="amharic")

    with pytest.raises(ValueError, match=r"Strength should be one of the following .*"):
        assert generate_mnemonic(strength=129)
