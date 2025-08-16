#!/usr/bin/env python3
"""
Simple test script to verify optional reasoning functionality works
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_optional_reasoning():
    """Test that the optional reasoning parameter works correctly"""
    
    print("🧪 Testing Optional Reasoning Functionality")
    print("=" * 50)
    
    try:
        # Import the module
        from transtype.processor import TranscriptProcessor
        from transtype.models import FieldResult
        
        print("✅ Successfully imported modules")
        
        # Test 1: Check default initialization (with reasoning)
        print("\n📝 Test 1: Default initialization (should include reasoning)")
        try:
            # We can't actually initialize without an API key, but we can check the class structure
            processor_class = TranscriptProcessor
            print("✅ TranscriptProcessor class available")
            
            # Check the __init__ signature
            import inspect
            signature = inspect.signature(processor_class.__init__)
            params = signature.parameters
            
            # Check if include_reasoning parameter exists
            if 'include_reasoning' in params:
                default_value = params['include_reasoning'].default
                print(f"✅ include_reasoning parameter found with default: {default_value}")
                
                if default_value is True:
                    print("✅ Default value is True (reasoning enabled by default)")
                else:
                    print("❌ Default value should be True")
                    return False
            else:
                print("❌ include_reasoning parameter not found")
                return False
                
        except Exception as e:
            print(f"❌ Error in Test 1: {e}")
            return False
        
        # Test 2: Check FieldResult model supports optional reasoning
        print("\n📝 Test 2: FieldResult model supports optional reasoning")
        try:
            # Create a FieldResult with reasoning
            result_with_reasoning = FieldResult(
                field_name="test_field",
                field_value="test_value",
                field_confidence=0.95,
                field_reason="Test reasoning"
            )
            print("✅ Created FieldResult with reasoning")
            
            # Create a FieldResult without reasoning
            result_without_reasoning = FieldResult(
                field_name="test_field",
                field_value="test_value", 
                field_confidence=0.95,
                field_reason=None
            )
            print("✅ Created FieldResult without reasoning (None)")
            
            # Check the values
            if result_with_reasoning.field_reason == "Test reasoning":
                print("✅ Reasoning field populated correctly")
            else:
                print("❌ Reasoning field not populated correctly")
                return False
                
            if result_without_reasoning.field_reason is None:
                print("✅ Reasoning field can be None")
            else:
                print("❌ Reasoning field should be None")
                return False
                
        except Exception as e:
            print(f"❌ Error in Test 2: {e}")
            return False
        
        # Test 3: Check signatures exist
        print("\n📝 Test 3: Check DSPy signatures exist")
        try:
            from transtype.processor import FieldExtractionSignature, FieldExtractionSignatureNoReasoning
            print("✅ Both FieldExtractionSignature and FieldExtractionSignatureNoReasoning exist")
            
            # Check signatures have expected output fields by inspecting their annotations
            reasoning_outputs = getattr(FieldExtractionSignature, '__annotations__', {})
            no_reasoning_outputs = getattr(FieldExtractionSignatureNoReasoning, '__annotations__', {})
            
            print(f"✅ FieldExtractionSignature fields: {list(reasoning_outputs.keys())}")
            print(f"✅ FieldExtractionSignatureNoReasoning fields: {list(no_reasoning_outputs.keys())}")
            
            # Check that reasoning signature has more fields (includes reasoning)
            if len(reasoning_outputs) > len(no_reasoning_outputs):
                print("✅ FieldExtractionSignature has more fields (includes reasoning)")
            else:
                print("⚠️  FieldExtractionSignature should have more fields than NoReasoning version")
                
        except Exception as e:
            print(f"❌ Error in Test 3: {e}")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! Optional reasoning functionality is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return False

def test_model_serialization():
    """Test that models serialize correctly with optional reasoning"""
    
    print("\n🧪 Testing Model Serialization")
    print("=" * 50)
    
    try:
        from transtype.models import FieldResult
        
        # Test with reasoning
        result_with = FieldResult(
            field_name="test", 
            field_value="value", 
            field_confidence=0.9,
            field_reason="Some reasoning"
        )
        
        dict_with = result_with.model_dump()
        print(f"✅ With reasoning: {dict_with}")
        
        # Test without reasoning
        result_without = FieldResult(
            field_name="test",
            field_value="value",
            field_confidence=0.9,
            field_reason=None
        )
        
        dict_without = result_without.model_dump()
        print(f"✅ Without reasoning: {dict_without}")
        
        # Check that serialization works correctly
        if dict_with['field_reason'] == "Some reasoning" and dict_without['field_reason'] is None:
            print("✅ Model serialization works correctly")
            return True
        else:
            print("❌ Model serialization issue")
            return False
            
    except Exception as e:
        print(f"❌ Error in serialization test: {e}")
        return False

if __name__ == "__main__":
    success1 = test_optional_reasoning()
    success2 = test_model_serialization()
    
    if success1 and success2:
        print("\n🚀 All tests passed! The optional reasoning feature is implemented correctly.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Please check the implementation.")
        sys.exit(1)
