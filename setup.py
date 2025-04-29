from setuptools import setup, find_packages

setup(
    name="SkyWarr",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame>=2.0.0",
        "pillow>=8.0.0",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "skywarr=main:main",
        ],
    },
    author="SkyWarr Developer",
    author_email="developer@example.com",
    description="A space shooter game with single and multiplayer modes",
    keywords="pygame, game, shooter, multiplayer",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Arcade",
    ],
)
