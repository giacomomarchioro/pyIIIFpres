import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyIIIFpres",
    version="0.4.0",
    author="Giacomo Marchioro",
    author_email="giacomomarchioro@outlook.com",
    description="A tool for easing the construction of JSON manifests compliant with IIIF API 3.0.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/giacomomarchioro/pyIIIFpres",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
