from setuptools import setup, find_packages

setup(
    name='kempner',
    version="0.0.1",
    packages=find_packages(include=["pykempner*"]),
    author='Thomas Schmelzer',
    author_email='thomas.schmelzer@gmail.com',
    description='', install_requires=['numpy', 'pandas==0.24.1']
)


