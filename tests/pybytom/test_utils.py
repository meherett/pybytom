#!/usr/bin/env python3

from pybytom.utils import (
    generate_mnemonic, generate_entropy, is_mnemonic, get_mnemonic_language, is_address, is_vapor_address
)

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


def test_address_and_vapor_address():

    assert is_address("bm1qp5wf088y45flgapfgzd4ngahpx86luttv8d8a5")
    assert is_address("bm1qp5wf088y45flgapfgzd4ngahpx86luttv8d8a5", "mainnet")
    assert is_address("sm1qp5wf088y45flgapfgzd4ngahpx86luttdk8xa6")
    assert is_address("sm1qp5wf088y45flgapfgzd4ngahpx86luttdk8xa6", "solonet")
    assert is_address("tm1qp5wf088y45flgapfgzd4ngahpx86luttg3vra9")
    assert is_address("tm1qp5wf088y45flgapfgzd4ngahpx86luttg3vra9", "testnet")

    assert is_vapor_address("vp1qp5wf088y45flgapfgzd4ngahpx86lutt8xa6cz")
    assert is_vapor_address("vp1qp5wf088y45flgapfgzd4ngahpx86lutt8xa6cz", "mainnet")
    assert is_vapor_address("sp1qp5wf088y45flgapfgzd4ngahpx86lutt0rljcf")
    assert is_vapor_address("sp1qp5wf088y45flgapfgzd4ngahpx86lutt0rljcf", "solonet")
    assert is_vapor_address("tp1qp5wf088y45flgapfgzd4ngahpx86lutt2y5hck")
    assert is_vapor_address("tp1qp5wf088y45flgapfgzd4ngahpx86lutt2y5hck", "testnet")

    with pytest.raises(TypeError, match="address must be string format"):
        assert is_address(1234567890)

    with pytest.raises(TypeError, match="address must be string format"):
        assert is_vapor_address(1234567890)

    with pytest.raises(TypeError, match="network must be string format"):
        assert is_address("bm1qp5wf088y45flgapfgzd4ngahpx86luttv8d8a5", 1234567890)

    with pytest.raises(TypeError, match="network must be string format"):
        assert is_vapor_address("vp1qp5wf088y45flgapfgzd4ngahpx86lutt8xa6cz", 1234567890)

    with pytest.raises(ValueError,
                       match="invalid network, use only this options mainnet, solonet or testnet networks."):
        assert is_address("bm1qp5wf088y45flgapfgzd4ngahpx86luttv8d8a5", "network")

    with pytest.raises(ValueError,
                       match="invalid network, use only this options mainnet, solonet or testnet networks."):
        assert is_vapor_address("vp1qp5wf088y45flgapfgzd4ngahpx86lutt8xa6cz", "network")
