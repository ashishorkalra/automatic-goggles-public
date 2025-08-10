from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="automatic-goggles",
    version="0.1.0",
    author="Ashish Kalra",
    author_email="ashishorkalra@gmail.com",
    description="A package for extracting structured fields from call transcripts with confidence scores",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ashishorkalra/automatic-goggles",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "dspy-ai>=2.3.7",
        "openai>=1.0.0",
        "pydantic>=2.0.0",
    ],
    keywords="transcript processing, field extraction, AI, natural language processing",
)
