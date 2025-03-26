#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="kiteclient",
    version="0.1",
    description="Client to interact with kite api",
    author="JSR Analytics",
    url="https://jsranalytics.tech",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["kiteclient"],
    install_requires=[
        "pyotp",
        "backoff"
    ],
    extras_require={
    },
    packages=find_packages(exclude=["tests"]),
    package_data={"schemas": ["tap_yotpo/schemas/*.json"]},
    include_package_data=True,
)