from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup_requirements = ["pytest-runner", "flake8-plugin-utils"]


setup(
    author="Petr Alekseev",
    author_email="petrmissial@gmail.com",
    classifiers=[
        "Framework :: Pytest",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Flake8 plugin to check allure decorators on test classes and methods",
    license="MIT license",
    include_package_data=True,
    keywords=["flake8", "pytest", "py.test", "allure"],
    name="flake8_allure_tree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["flake8_allure_tree"]),
    setup_requires=setup_requirements,
    version="0.0.1",
    zip_safe=False,
    entry_points={
        "flake8.extension": [
            "AL = flake8_allure_tree.flake8_allure:AllurePytestPlugin",
        ],
    },
    install_requires=["pytest", "flake8_plugin_utils"],
)
