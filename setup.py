import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nsga-ii-easy-nikanj", # Replace with your own username
    version="0.0.1",
    description="short implementation of the nsga-ii algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaBeKro/nsga-ii-easy",

    
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

    test_suite="tests",

    # extras_require={
    #     "dev": ["pytest >= 3.7"],
    # }
)