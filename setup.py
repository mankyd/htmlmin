from setuptools import setup, find_packages
from htmlmin import __version__

README = open('README.md').read()

setup(
    name='htmlmin',
    version=__version__,
    description='An HTML Minifier',
    long_description=README,
    author='Dave Mankoff',
    author_email='mankyd@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    test_suite='htmlmin.tests.tests.suite',
    install_requires=[],
    tests_require=[],
    entry_points={
        'console_scripts': [
            'htmlmin = htmlmin.command:main',
        ],
    },
)
