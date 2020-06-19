from cryptography.fernet import Fernet, InvalidToken
import pytest

from alvinchow.lib.encryption import FernetEngine, MultiFernetEngine


def test_fernet_engine():
    key = Fernet.generate_key()
    f = FernetEngine(key)
    message = 'Something secret'
    token = f.encrypt(message)
    assert f.decrypt(token) == message

    # Check wrong key will not work
    key2 = Fernet.generate_key()
    f2 = FernetEngine(key2)
    with pytest.raises(InvalidToken):
        f2.decrypt(token)


def test_multi_fernet_engine():
    key1 = Fernet.generate_key()
    key2 = Fernet.generate_key()

    f1 = MultiFernetEngine([key1])
    message = 'Some secret thing'
    token = f1.encrypt(message)
    assert f1.decrypt(token) == message

    # Test key rotation
    f2 = MultiFernetEngine([key2, key1])
    assert f2.decrypt(token) == message
    new_token = f2.rotate(token)

    with pytest.raises(InvalidToken):
        f1.decrypt(new_token)
