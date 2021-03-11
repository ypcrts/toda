from setuptools import setup

setup(
    name="toda",
    packages=["toda"],
    version="0.0.1",
    description=(
        "Toda gives you"
        " the power to safely deploy files using symlinks on any"
        " operating system with Python installed."
    ),
    install_requires=[""],
    author="ypcrts",
    author_email="ypcrts",
    url="https://github.com/ypcrts/toda",
    keywords=["dotfiles", "symlink", "environment"],
    license="MPL 2.0",
    classifiers=[
        'Development Status :: 4 - Beta',
        # "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    entry_points={"console_scripts": ["toda=toda.__main__:main"]},
)
