from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="brutal-bag",
    description="A js-optional frontend for Wallabag",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Tristan Havelick",
    url="https://github.com/thavelick/brutal-bag",
    project_urls={
        "Issues": "https://github.com/thavelick/brutal-bag/issues",
        "CI": "https://github.com/thavelick/brutal-bag/actions",
        "Changelog": "https://github.com/thavelick/brutal-bag/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["brutal_bag"],
    entry_points="""
        [console_scripts]
        brutal-bag=brutal_bag.cli:cli
    """,
    install_requires=["click", "flask", "httpx"],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.7",
    package_data={"brutal_bag": ["templates/*.html"]},
    include_package_data=True,
)
