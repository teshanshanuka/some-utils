# Author: Teshan Liyanage <teshanuka@gmail.com>

import setuptools

with open("README.md") as fp:
    long_description = fp.read()

with open("requirements.txt") as fp:
    install_requires = fp.read().strip().splitlines()

with open("some_utils/__init__.py") as fd:
    exec("".join(l for l in fd if l.startswith("__")))

setuptools.setup(
    name="some_utils",  # Some name for the package
    version=__version__,
    author=__author__,
    author_email="teshanuka@gmail.com",
    description="Some useful utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['some_utils'],
    python_requires='>=3.8',
    install_requires=install_requires
)
