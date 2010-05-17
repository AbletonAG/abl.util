from textwrap import dedent
from setuptools import setup, find_packages


TEST_REQUIREMENTS = ["nose"]

setup(
    name = "AbletonUtil",
    version = "0.1",
    author = "Diez B. Roggisch",
    author_email = "diez.roggisch@ableton.com",
    description = dedent("""
    A package that contains various helpful classes and functions
    used widely in the Ableton Python code base.
    """),
    packages = find_packages(),
    namespace_packages = ["abl"],
    install_requires = [
        ],
    extras_require = dict(
        testing=TEST_REQUIREMENTS,
        ),
    tests_require=TEST_REQUIREMENTS,
)

