from setuptools import setup, find_packages


setup(
    name="dgg-bot",
    version="0.1.4",
    author="Fritz",
    description="A library for making a bot in Destiny.gg chat.",
    long_description_content_type="text/markdown",
    url="https://github.com/Fritz-02/dgg-bot/",
    project_urls={
        "Bug Tracker": "https://github.com/Fritz-02/dgg-bot/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Communications :: Chat"
    ],
    packages=find_packages(),
    python_requires=">=3.7",
)