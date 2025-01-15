from setuptools import setup, find_packages
from pathlib import Path



setup(
    name="bettercli",
    version="0.0.1",
    description="A better CLI library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/r5dan/better-cli",
    author="R5dan",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT",
        "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",


        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",

        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    platforms=["any"],
    keywords="cli, command line, command-line, interface, library, tool, better, python, python3, cli-library, cli-tool, cli-interface, cli-library, better-cli",
    packages=find_packages(exclude=["contrib", "docs", "tests", "examples"]),
    install_requires=[],
    extras_require={}
)
