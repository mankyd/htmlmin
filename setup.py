import os
from setuptools import setup, find_packages

from htmlmin import __version__

here = os.path.dirname(__file__)

README = open(os.path.join(here, 'README.rst')).read()
LICENSE = open(os.path.join(here, 'LICENSE')).read()

setup(
    name='htmlmin',
    version=__version__,
    license='BSD',
    description='An HTML Minifier',
    long_description=README,
    url='https://htmlmin.readthedocs.io/en/latest/',
    download_url='https://github.com/mankyd/htmlmin',
    author='Dave Mankoff',
    author_email='mankyd@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    test_suite='htmlmin.tests.tests.suite',
    install_requires=[],
    tests_require=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    entry_points={
        'console_scripts': [
            'htmlmin = htmlmin.command:main',
        ],
    },
)
