from alvinchow.lib.data import SimpleEnum


def test_simple_enum():
    class Color(SimpleEnum):
        RED = 'red'
        GREEN = 'green'
        BLUE = 'blue'

    assert Color.RED == 'red'
    assert 'red' in Color
    assert list(Color) == ['red', 'green', 'blue']
