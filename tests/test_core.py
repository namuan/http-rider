from httprider.core import abbreviate


def test_abbreviate():
    assert abbreviate("Hello World", 5) == "Hello ..."
