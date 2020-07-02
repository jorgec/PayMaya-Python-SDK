import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='PayMaya Python SDK',
    version='0.1',
    scripts=['paymaya_sdk.py'],
    author="Jorge Cosgayon",
    author_email="jorge.cosgayon@gmail.com",
    description="A Python port of the PHP PayMaya SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jorgec/PayMaya-Python-SDK",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
