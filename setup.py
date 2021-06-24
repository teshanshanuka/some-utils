# Author: Teshan Liyanage <teshanuka@gmail.com>

import setuptools
import some_utils

with open("README.md") as fp:
    long_description = fp.read()

with open("requirements.txt") as fp:
    install_requires = fp.read().strip().splitlines()

setuptools.setup(
    name="some_utils",  # Some name for the package
    version=some_utils.__version__,
    author="Teshan Liyanage",
    author_email="teshanuka@gmail.com",
    description="Some useful utilities by Teshan Liyanage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['some_utils'],
    python_requires='>=3.8',
    install_requires=install_requires
)
