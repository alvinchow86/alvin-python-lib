from setuptools import setup

# get version
version = '0.0.1'

setup(
    name='alvin-python-lib',
    version=version,
    description="Useful Python utilities and libraries for app development",
    packages=[
        'alvinchow/lib',
        'alvinchow/lib/config',
    ],
    package_data={},
    scripts=[],
    install_requires=[
        'python-dateutil>=2.7'
    ],
)
