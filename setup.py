from setuptools import setup, find_packages

def get_requirements():
    requirements = []
    with open('requirements.txt') as req_file:
        source = req_file.read()
        if source:
            requirements = source.splitlines()
    return requirements

with open('README.md') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

setup(
    name='instpector',
    version='0.1.0',
    description='The Instagram web command line interface',
    long_description=README,
    author='Erik Lopez',
    url='https://github.com/niuware/instpector',
    license=LICENSE,
    packages=find_packages(exclude=('examples', 'tests')),
    install_requires=get_requirements()
)
