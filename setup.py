from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
from codecs import open

from bggcli.version import VERSION


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        pytest.main(self.test_args)

# long description
with open('README.rst', 'r', encoding='utf8') as f:
    long_description = f.read()

setup(
    author='Sylvain Francois',
    author_email='syllant@gmail.com',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Games/Entertainment :: Board Games"
    ],
    cmdclass={'test': PyTest},
    description='Command Line Interface for BoardGameGeek.com',
    entry_points='''
        [console_scripts]
        bggcli=bggcli.main:main
    ''',
    install_requires=[
        'selenium', 'docopt'
    ],
    keywords='bgg boardgamegeek',
    license='MIT',
    long_description=long_description,
    name='bggcli',
    packages=find_packages(),
    py_modules=['bggcli'],
    tests_require=["pytest"],
    test_suite='test',
    url='http://github.org/syllant/bggcli',
    version=VERSION
)
