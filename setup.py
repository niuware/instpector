from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    README = f.read()

setup(
    name='instpector',
    version='0.1.1',
    description='The Instagram web command line interface',
    author='Erik Lopez',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/niuware/instpector',
    download_url='https://github.com/niuware/instpector/archive/0.1.1.tar.gz',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=('examples', 'tests')),
    install_requires=['requests']
)
