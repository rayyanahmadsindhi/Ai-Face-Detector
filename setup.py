#!/usr/bin/env python3
"""
Setup script for AI Face Detection Application
"""

from setuptools import setup, find_packages

with open("README_PYTHON.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-face-detector",
    version="1.0.0",
    author="AI Assistant",
    author_email="",
    description="Real-time face detection application with GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics :: Capture :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=[
        "opencv-python>=4.5.0",
        "Pillow>=8.0.0",
        "numpy>=1.19.0",
    ],
    entry_points={
        "console_scripts": [
            "face-detector=face_detector:main",
        ],
    },
)
