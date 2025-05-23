from setuptools import setup, find_packages
import platform

# Determine platform-specific dependencies
platform_deps = []
if platform.system() == "Windows":
    platform_deps.append("pywin32")

setup(
    name="phoenix-recovery",
    version="1.0.0",
    description="Advanced Data Recovery Tool for Ransomware and Corruption",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "rich>=10.0.0",
    ] + platform_deps,
    entry_points={
        "console_scripts": [
            "phoenix=pheonix:main",
            "phoenix-gui=phoenix_gui:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: X11 Applications :: GTK",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: System :: Recovery Tools",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
) 