#!/usr/bin/env python
from os.path import basename
from os.path import splitext
from glob import glob
from setuptools import setup, find_packages

setup(
    name="python_test",
    packages=find_packages("src"),
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    package_dir={"": "src"},
    package_data={'web.templates': ['index.html']},
    version="1.0.0",
    python_requires=">=3.5",
    install_requires=[
        "PyGithub>=1.54.1",
        "PyYAML>=5.4b2",
        "flask>=1.1.2"
    ],
    zip_safe=True,
    extra_require={
        "dev": [
            "pytest",
            "pytest-pep8",
            "pytest-cov"
        ]
    }
)
