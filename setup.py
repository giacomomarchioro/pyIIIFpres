import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyIIIFpres",
    version="0.0.61",
    author="Giacomo Marchioro",
    author_email="giacomomarchioro@outlook.com",
    description="A tool creating JSON manifests complaint with IIIF presentation API 3.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/giacomomarchioro/pyIIIFpres",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)