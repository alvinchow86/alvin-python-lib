from setuptools import setup

# get version
version = '0.0.5'

setup(
    name='alvin-python-lib',
    version=version,
    description="Useful Python utilities and libraries for app development",
    packages=[
        'alvinchow/lib',
        'alvinchow/lib/config',
        'alvinchow/lib/remote',
        'alvinchow/redis',
        'alvinchow/redis/cache',
        'alvinchow/sqlalchemy',
        'alvinchow/sqlalchemy/types',
        'alvinchow/pytest',
    ],
    package_data={},
    entry_points={
        'pytest11': [
            'alvinchow = alvinchow.pytest.plugin',
        ],
    },
    scripts=[],
    install_requires=[
        'python-dateutil>=2.7'
    ],
    extras_require={
        'encryption': ["cryptography>=3.2"],
    },
)
