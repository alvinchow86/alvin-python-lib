from setuptools import setup

# get version
version = '0.0.2'

setup(
    name='alvin-python-lib',
    version=version,
    description="Useful Python utilities and libraries for app development",
    packages=[
        'alvinchow/lib',
        'alvinchow/lib/config',
        'alvinchow/lib/remote',
        'alvinchow/redis',
        'alvinchow/sqlalchemy',
        'alvinchow/sqlalchemy/types',
    ],
    package_data={},
    scripts=[],
    install_requires=[
        'python-dateutil>=2.7'
    ],
    extras_require={
        'encryption': ["cryptography>=2.7"],
    },
)
