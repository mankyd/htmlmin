from setuptools import setup, find_packages
from htmlmin import __version__

README = open('README.md').read()

setup(
    name='htmlmin',
    version=__version__,
    description='An HTML Minifier',
    long_description=README,
    url='https://htmlmin.readthedocs.org/en/latest/',
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
        "Programming Language :: Python :: 2.6",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    entry_points={
        'console_scripts': [
            'htmlmin = htmlmin.command:main',
        ],
    },
)
