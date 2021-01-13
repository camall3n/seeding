from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="seeding",
    version="0.1.0",
    description="Lightweight python library for achieving deterministic random seeds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cameron Allen",
    author_email=("csal@brown.edu"),
    packages=find_packages(include=["seeding", "seeding.*"]),
    # scripts=["bin/seeding"],
    url="https://github.com/camall3n/seeding/",
    # install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
