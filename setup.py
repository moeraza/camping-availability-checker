from __future__ import annotations

import pathlib

from setuptools import find_packages
from setuptools import setup

current_dir = pathlib.Path(__file__).parent
readme = (current_dir / 'README.md').read_text()
version = (current_dir / 'VERSION').read_text().strip()


def read_requirements():
    with open('requirements.txt') as f:
        requirements = f.readlines()
        requirements = [req.strip() for req in requirements if not req.startswith(('#', '\n'))]
    return requirements


setup(
    name='camping-availability-checker',
    version=version,
    description='code to get camping availability',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=['Progmramming Language :: Python'],
    packages=find_packages(),
    install_requires=read_requirements(),
)
