from setuptools import setup

with open("requirements.freeze.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    install_requires=requirements
)
