from setuptools import find_packages, setup

package_name = "square_authentication_helper"

setup(
    name=package_name,
    version="2.5.2",
    packages=find_packages(),
    install_requires=["square_commons>=2.0.0", "square_database_structure>=2.5.7"],
    author="thePmSquare",
    author_email="thepmsquare@gmail.com",
    description="helper to access the authentication layer for my personal server.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url=f"https://github.com/thepmsquare/{package_name}",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
