from usaddress import _tokenFeatures


def test_unicode():
    features = _tokenFeatures("å")
    assert features["endsinpunc"] is False
