from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='chessboardCLI',
    version='1.0.12',
    description='Chessboard generator in command line',
    url='https://github.com/houluy/chessboard',
    author='Houlu',
    author_email='houlu8674@bupt.edu.cn',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='chessboard',
    packages=['chessboard',],
    install_requires=[
        'colorline',
    ],
    python_requires='>=3',
)
