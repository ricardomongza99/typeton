from setuptools import setup, find_packages

setup(
    name='typeton',
    version='0.1.0',
    packages=find_packages(include=['typeton', 'src.*']),
    install_requires=[
        'jsonpickle>=2.2.0',
    ]
)