from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    requirements = fr.read().splitlines()

setup(
    name="voxcharta-my-voting-record",
    version="0.3.2",
    packages=["voxcharta_my_voting_record"],
    scripts=["bin/vox_run"],
    url="https://github.com/astrochun/voxcharta-my-voting-record",
    license="GNU GPLv3",
    author="Chun Ly",
    author_email="astro.chun@gmail.com",
    description="A Python tool to extract information from VoxCharta My Voting Records HTML",  # noqa: E501
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
