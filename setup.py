# Setup.py file
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required_libs = f.read().splitlines()

setuptools.setup(name="pyassume",
                 version='0.0.8',
                 author="Kenneth Leung",
                 author_email="pyassume@outlook.com",
                 description="PyAssume - Automated Assumption Checks for Regression Models",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/kennethleungty/pyassume",
                 classifiers=[
                             "Programming Language :: Python :: 3",
                             "License :: OSI Approved :: MIT License",
                             "Operating System :: OS Independent",
                 ],
                 package_dir={"": "src"},
                 packages=setuptools.find_packages("src"),
                 python_requires=">=3.7",
                 include_package_data=True,
                 install_requires=required_libs
                 )
