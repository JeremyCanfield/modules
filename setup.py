from setuptools import setup

from snspublish import __version__

setup(
    name='snspublish',
    version=__version__,

    url='https://github.com/JeremyCanfield/modules',
    author='Jeremy Canfield',
    author_email='jeremy.canfield@freekb.net',

    py_modules=['snspublish'],
    install_requires=[
        "boto3 >= 1.28.45",
    ],    
)
