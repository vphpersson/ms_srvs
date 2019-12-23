from setuptools import setup, find_packages
setup(
    name='ms_srvs',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'rpc @ http://github.com/vphpersson/rpc/tarball/master'
    ]
)
