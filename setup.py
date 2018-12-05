#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Chris Knott, Bruno Martin",
    author_email='martin.bruno.mail@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="eel fork optimized for a transcrypt frontend",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='eel_for_transcrypt',
    name='eel_for_transcrypt',
    packages=find_packages(include=['eel_for_transcrypt']),
    package_data={
        'eel_for_transcrypt': ['eel.js'],
    },
    install_requires=['bottle', 'bottle-websocket', 'future', 'whichcraft'],
    description='eel fork optimized for transcrypt',
    long_description=open('README.md', encoding='utf-8').readlines()[1],
    keywords=['gui', 'transcrypt', 'html', 'javascript', 'electron'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/brumar/eel_for_transcrypt',
    version='0.1.0',
    zip_safe=False,
)
