from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


with open("README.rst") as f:
    readme = f.read()


packages = find_packages()

extra_require = {"dev": ["black", "flake8"]}


setup(
    name="dgg-bot",
    version="0.10.1",
    author="Fritz",
    description="A library for making a bot in Destiny.gg chat.",
    long_description=readme,
    long_description_content_type="text/x-rst",
    license="MIT",
    url="https://github.com/Fritz-02/dgg-bot/",
    project_urls={
        "Bug Tracker": "https://github.com/Fritz-02/dgg-bot/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
    ],
    install_requires=requirements,
    extra_require=extra_require,
    packages=packages,
    python_requires=">=3.9",
)
