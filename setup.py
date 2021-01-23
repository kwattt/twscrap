from setuptools import setup, find_packages

with open("requirements.txt") as stream:
    install_requires = stream.read().splitlines()

setup(
    name='twscrap',
    version='0.0.1',
    description='A twitter scraper',
    license='MIT',
    packages=["twscrap"],
    author='kwattt',
    keywords=['Twitter', 'Scrap'],
    url='https://github.com/kwattt/twscrap'
)