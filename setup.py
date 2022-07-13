import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="battstats", # Replace with your own username
    version="0.0.1",
    author="Eric Ravet",
    author_email="ericr@battgenie.life",
    description="Calculate cycle stats from Arbin stream and upload to database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BattGenie/battstats.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)