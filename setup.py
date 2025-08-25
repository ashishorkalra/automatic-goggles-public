from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="automatic-goggles",
    version="0.3.0",
    author="Ashish Kalra",
    author_email="ashishorkalra@gmail.com",
    description="A package for extracting structured fields from call transcripts with confidence scores",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ashishorkalra/automatic-goggles",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9,<3.13",
    install_requires=[
        "dspy==2.6.8",
        "openai>=1.0.0",
        "pydantic>=2.0.0",
    ],
    keywords="transcript processing, field extraction, AI, natural language processing",
)
