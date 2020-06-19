from alvinchow.lib.logging import get_logger

logger = get_logger(__name__)

try:
    from cryptography.fernet import Fernet, MultiFernet
except ImportError:  # pragma: no cover
    print('Please install cryptography module')
    raise


class FernetEngine:
    """
    Loose wrapper around Fernet to handl string <-> byte conversion.
    Loosely based off of code in sqlalchemy-utils
    """
    def __init__(self, key):
        self.fernet = Fernet(key)

    def encrypt(self, val) -> bytes:
        if isinstance(val, str):
            val = val.encode()
        encrypted_bytes = self.fernet.encrypt(val)
        return encrypted_bytes

    def decrypt(self, val) -> str:
        decrypted_bytes = self.fernet.decrypt(val)
        decrypted_string = decrypted_bytes.decode('utf-8')
        return decrypted_string


class MultiFernetEngine(FernetEngine):
    def __init__(self, keys):
        fernets = [Fernet(key) for key in keys]
        self.fernet = MultiFernet(fernets)
        self.sub_fernets = fernets

    def rotate(self, token):
        return self.fernet.rotate(token)
