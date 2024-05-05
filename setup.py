from setuptools import setup

from my_pip_package import __version__

setup(
    name='my_pip_package',
    version=__version__,

    url='https://github.com/JeremyCanfield/modules',
    author='Jeremy Canfield',
    author_email='jeremy.canfield@freekb.net',

    py_modules=['my_pip_package'],
)
