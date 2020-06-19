from sqlalchemy import types

encryption = None
try:
    from alvinchow.lib import encryption
    from alvinchow.lib.encryption import FernetEngine, MultiFernetEngine
except ImportError:   # pragma: no cover
    pass


class EncryptedText(types.TypeDecorator):
    impl = types.LargeBinary

    def __init__(self, engine=None, key=None, keys=None, preprocess=None, **kwargs):
        if not encryption:   # pragma: no cover
            raise Exception('Please install encryption dependencies')

        super().__init__()

        if engine:
            self.engine = engine
        elif keys:
            self.engine = MultiFernetEngine(keys)
        elif key:
            self.engine = FernetEngine(key)

        self.preprocess_func = preprocess

    def process_bind_param(self, value, dialect):
        if value:
            if self.preprocess_func:
                value = self.preprocess_func(value)

            value = self.engine.encrypt(value)
            return value

    def process_result_value(self, value, dialect):
        if value:
            value = self.engine.decrypt(value)
            return value
