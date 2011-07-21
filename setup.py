from setuptools import setup, find_packages


TEST_REQUIREMENTS = ["nose"]

setup(
    name = "abl.util",
    version = "0.1.5",
    author = "Diez B. Roggisch",
    author_email = "diez.roggisch@ableton.com",
    description = "A package that contains various helpful classes and functions used widely in the Ableton Python code base.",
    license="MIT",
    packages = find_packages(),
    namespace_packages = ["abl"],
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

