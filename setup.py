import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytron",
    version="0.0.1",
    author="PyCamp AR 2022",
    description="Pytron game - Tron game for python bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arielrossanigo/pytron",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["pytron"],
    python_requires=">=3.6",
    install_requires=[
        "click",
    ],
    entry_points={
        'console_scripts': [
            'pytron=pytron.__main__:main',
        ],
    },
)
