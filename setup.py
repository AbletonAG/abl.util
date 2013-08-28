import versioneer

from setuptools import setup, find_packages

versioneer.versionfile_source = "abl/util/_version.py"
versioneer.versionfile_build = versioneer.versionfile_source
versioneer.tag_prefix = ""
versioneer.parentdir_prefix = "abl.util"


TEST_REQUIREMENTS = ["nose"]

setup(
    name = "abl.util",
    version = versioneer.get_version(),
    author = "Diez B. Roggisch",
    author_email = "diez.roggisch@ableton.com",
    description = "A package that contains various helpful classes and functions used widely in the Ableton Python code base.",
    license="MIT",
    packages=find_packages(exclude=['test']),
    #namespace_packages = ["abl"],
    install_requires = [
        ],
    extras_require = dict(
        testing=TEST_REQUIREMENTS,
        ),
    tests_require=TEST_REQUIREMENTS,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
    zip_safe=False,
)

