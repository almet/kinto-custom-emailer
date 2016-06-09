import platform
import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def read_file(filename):
    """Open a related file and return its content."""
    with codecs.open(os.path.join(here, filename), encoding='utf-8') as f:
        content = f.read()
    return content

README = read_file('README.rst')

REQUIREMENTS = []
DEPENDENCY_LINKS = []


setup(name='kinto-custom-emailer',
      version='0.0.1',
      description='Kinto custom emailer',
      long_description=README,
      license='Apache License (2.0)',
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: Implementation :: CPython",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          "License :: OSI Approved :: Apache Software License"
      ],
      keywords="web sync json storage services",
      author='Alexis Métaireau',
      author_email='alexis@notmyidea.org',
      url='https://github.com/almet/kinto-custom-emailer',
      packages=find_packages(),
      package_data={'': ['*.rst', '*.py']},
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIREMENTS,
      dependency_links=DEPENDENCY_LINKS)
