from setuptools import setup

# get version
__version__ = None
exec(open('alvinchow/lib/version.py').read())

setup(
    name='alvinchow-lib',
    version=__version__,
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
