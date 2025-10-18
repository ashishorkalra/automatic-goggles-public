"""
Test script to validate package structure and imports without external dependencies
"""

import os
import sys


def test_package_structure():
    """Test that all required files exist"""
    required_files = [
        "setup.py",
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "requirements.txt",
        "transtype/__init__.py",
        "transtype/models.py",
        "transtype/processor.py",
        "tests/__init__.py",
        "tests/test_processor.py",
    ]

    print("Testing package structure...")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")


def test_model_imports():
    """Test that models can be imported and work correctly"""
    print("\nTesting model imports...")
    try:
        sys.path.insert(0, ".")
        from transtype.models import FieldResult, TranscriptInput, TranscriptOutput

        print("✓ All models imported successfully")

        # Test model validation
        test_data = {
            "messages": [{"role": "user", "content": "Hello"}],
            "fields": [
                {
                    "field_name": "test",
                    "field_type": "string",
                    "format_example": "example",
                    "field_description": "A test field description",
                }
            ],
        }
        validated = TranscriptInput(**test_data)
        print("✓ Model validation works")
        print(
            f"✓ Validated {len(validated.messages)} messages and {len(validated.fields)} fields"
        )

        # Test output model
        field_result = FieldResult(
            field_name="test",
            field_value="value",
            field_confidence=0.95,
            field_reason="Test reason",
        )
        TranscriptOutput(fields=[field_result])
        print("✓ Output models work correctly")

    except ImportError as e:
        print(f"✗ Import error: {e}")
    except Exception as e:
        print(f"✗ Validation error: {e}")


def test_package_metadata():
    """Test package metadata"""
    print("\nTesting package metadata...")
    try:
        sys.path.insert(0, ".")
        import transtype

        print(f"✓ Package version: {transtype.__version__}")
        print(f"✓ Available exports: {transtype.__all__}")
    except Exception as e:
        print(f"✗ Metadata error: {e}")


def main():
    """Run all tests"""
    print("Transtype Package Validation")
    print("=" * 40)

    test_package_structure()
    test_model_imports()
    test_package_metadata()

    print("\n" + "=" * 40)
    print("Validation complete!")
    print("\nTo install dependencies and test fully:")
    print("pip install -r requirements.txt")
    print("python example.py")


if __name__ == "__main__":
    main()
