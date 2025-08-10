# Deployment Guide for Automatic Goggles Package

## Prerequisites

1. **Python 3.8+** installed
2. **pip** and **setuptools** updated
3. **twine** for uploading to PyPI
4. **PyPI account** (register at https://pypi.org)
5. **TestPyPI account** (register at https://test.pypi.org) for testing

## Setup Steps

### 1. Install Build Tools

```bash
pip install --upgrade pip setuptools wheel twine build
```

### 2. Update Package Information

Before publishing, update the following files with your information:

**setup.py** and **pyproject.toml**:
- Replace `"Your Name"` with your actual name
- Replace `"your.email@example.com"` with your email
- Update the GitHub URL to your repository

### 3. Build the Package

```bash
# Navigate to package directory
cd /Users/ashishkalra/Documents/repos/transcribing_project/transtype_1

# Build the package
python -m build
```

This creates:
- `dist/automatic_goggles-0.1.0.tar.gz` (source distribution)
- `dist/automatic_goggles-0.1.0-py3-none-any.whl` (wheel distribution)

### 4. Test the Package Locally

```bash
# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Test the example
python example.py  # (after adding your OpenAI API key)
```

### 5. Upload to TestPyPI (Recommended First)

```bash
# Upload to TestPyPI first
python -m twine upload --repository testpypi dist/*
```

You'll be prompted for your TestPyPI username and password.

### 6. Test Installation from TestPyPI

```bash
# Create a new virtual environment for testing
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ automatic-goggles

# Test the installation
python -c "from transtype import TranscriptProcessor; print('Import successful!')"
```

### 7. Upload to PyPI (Production)

Once testing is successful:

```bash
# Upload to PyPI
python -m twine upload dist/*
```

### 8. Verify Installation

```bash
# Install from PyPI
pip install automatic-goggles

# Test
python -c "from transtype import TranscriptProcessor; print('Package installed successfully!')"
```

## Version Management

To release a new version:

1. Update version in `setup.py`, `pyproject.toml`, and `transtype/__init__.py`
2. Build new package: `python -m build`
3. Upload: `python -m twine upload dist/*`

## Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Consider using API tokens instead of passwords for PyPI uploads

## Automation (Optional)

For CI/CD, you can create GitHub Actions to automatically:
- Run tests on commits
- Build and publish on releases
- Check code quality

## Common Issues

1. **Package name conflicts**: Choose a unique name on PyPI
2. **Version conflicts**: Increment version numbers for each upload
3. **Missing dependencies**: Ensure all dependencies are listed correctly
4. **File permissions**: Make sure all files are readable

## Package Structure Summary

```
transtype/
├── setup.py                 # Package setup configuration
├── pyproject.toml          # Modern Python packaging config
├── README.md               # Package documentation
├── LICENSE                 # MIT license
├── MANIFEST.in            # Additional files to include
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Development dependencies
├── .gitignore             # Git ignore patterns
├── example.py             # Usage example
├── transtype/             # Main package directory
│   ├── __init__.py        # Package initialization
│   ├── models.py          # Pydantic data models
│   └── processor.py       # Core processing logic
└── tests/                 # Test directory
    ├── __init__.py
    └── test_processor.py  # Unit tests
```
