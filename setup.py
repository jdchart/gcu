from setuptools import setup
from setuptools import find_packages

long_description= """
# gcu
A collection of functions I use to make my Google Colab notebooks cleaner.
"""

required = [
    "requests", 
    "numpy"
]

setup(
    name="gcu",
    version="0.0.1",
    description="A collection of functions I use to make my Google Colab notebooks cleaner.",
    long_description=long_description,
    author="Jacob Hart",
    author_email="jacob.dchart@gmail.com",
    url="https://github.com/jdchart/gcu",
    install_requires=required,
    packages=find_packages()
)