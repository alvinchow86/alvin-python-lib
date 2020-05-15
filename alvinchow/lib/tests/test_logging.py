from alvinchow.lib.logging import get_logger


def test_logger():
    logger = get_logger('foo.bar')
    logger.info('works')
