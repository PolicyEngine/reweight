"""This file contains your country package's metadata and dependencies."""

from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="reweight",
    version="0.0.1",
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
    data_files=[
        (
            ["CHANGELOG.md", "LICENSE", "README.md"],
        ),
    ],
    install_requires=[
        "click==8.1.3",
        "h5py",
        "microdf_python",
        "pandas",
        "pathlib",
        "policyengine-core>=2.21.5,<2.22",
        "pytest",
        "pytest-dependency",
        "pyyaml",
        "requests",
        "scipy==1.10.1",
        "synthimpute",
        "tables==3.8.0",
        "tabulate",
        "torch",
        "tqdm",
    ],
    extras_require={
        "dev": [
            "autopep8",
            "black",
            "coverage",
            "furo==2022.9.29",
            "jupyter-book>=0.15,<0.16",
            "linecheck",
            "markupsafe",
            "plotly",
            "pydata-sphinx-theme==0.13.1",
            "setuptools",
            "sphinx>=5.0,<5.1",
            "sphinx-argparse",
            "sphinx-math-dollar",
            "wheel",
            "yaml-changelog",
            "survey-enhance",
        ],
    },
    # Windows CI requires Python 3.9.
    python_requires=">=3.7",
    packages=find_packages(),
)