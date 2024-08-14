"""This file contains metadata and dependencies."""

from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="reweight",
    version="0.3.0",
    author="PolicyEngine",
    author_email="hello@policyengine.org",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    description="Reweighting library for survey data for use with PolicyEngine",
    keywords="benefit microsimulation social tax",
    license="http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    url="https://github.com/PolicyEngine/reweight",
    include_package_data=True,  # Will read MANIFEST.in
    install_requires=[
        "numpy<2.0",
        "pandas",
        "torch",
        "tensorboard",
        "jupyter-book",
        "pytest",
        "policyengine-core~=2.21.8",
        "policyengine-us~=0.794.1",
        "policyengine-uk",
        "survey_enhance",
    ],
    extras_require={
        "dev": [
            "black",
            "yaml-changelog",
            "setuptools",
            "setuptools_scm",
        ],
    },
    # Windows CI requires Python 3.9.
    python_requires=">=3.7",
    packages=find_packages(),
)
