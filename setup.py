import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


def parse_requirements(filename: str):
    with open(filename, "r") as file:
        return file.read().splitlines()


setup(
    name="spd-columns-check",
    version="0.1.0",
    description="A short description of the project.",
    author="Mia Pham",
    packages=find_packages(),
    include_package_data=True,
    long_description=README,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "spd-columns-check=src.interface.cli.cli:cli",
        ],
    },
    install_requires=parse_requirements("requirements.txt"),
    extras_require={
        "dev": parse_requirements("requirements.dev.txt"),
    },
    zip_safe=False,
    license="MIT",
)
