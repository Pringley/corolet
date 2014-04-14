from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup
setup(
    name = "corolet",
    version = "0.0.1",
    py_modules = ['corolet'],
    
    author = "Ben Pringle",
    author_email = "ben.pringle@gmail.com",
    url = "http://github.com/Pringley/corolet",
    description = "Use greenlets as coroutines in asyncio",
    license = "MIT",
)
