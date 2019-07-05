from setuptools import setup, find_packages

def get_requirements():
    requirements = []
    with open('requirements.txt', 'r') as req_file:
        source = req_file.read()
        if source:
            requirements = source.splitlines()
    return requirements

setup(
    name='instpector',
    version='0.1.0',
    description='The Instagram web command line interface',
    author='Erik Lopez',
    url='https://github.com/niuware/instpector',
    download_url='https://github.com/niuware/instpector/archive/0.1.0.tar.gz',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=('examples', 'tests')),
    install_requires=get_requirements()
)
