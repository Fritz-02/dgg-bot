from setuptools import setup, find_packages


setup(
    name="dgg-bot",
    version="0.1.2",
    author="Fritz",
    description="A library for making a bot in Destiny.gg chat.",
    long_description_content_type="text/markdown",
    url="https://github.com/Fritz-02/dgg-bot/",
    project_urls={
        "Bug Tracker": "https://github.com/Fritz-02/dgg-bot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
)