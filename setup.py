PACKAGE      = "pyos"
NAME         = PACKAGE
DESCRIPTION  = "Python Linux system operation lib"
AUTHOR       = "galileo-project"
AUTHOR_EMAIL = "vwenjie@hotmail.com"
URL          = "http://galileo-project.github.io/#/pyos"
LICENSE      = "MIT License"
VERSION      = __import__(PACKAGE).__version__

from setuptools import setup, find_packages

setup(name         = NAME,
      version      = VERSION,
      description  = DESCRIPTION,
      author       = AUTHOR,
      author_email = AUTHOR_EMAIL,
      license      = LICENSE,
      url          = URL,
      packages     = find_packages(exclude=["test"]))