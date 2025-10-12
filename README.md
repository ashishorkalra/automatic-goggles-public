# Automatic Goggles

A Python package for extracting structured fields from call transcripts with confidence scores using DSPy and OpenAI's language models.

## Features

- Extract structured fields from conversation transcripts
- **Evaluate conversation quality** with assertion-based scoring
- **Contextual field descriptions** - Provide detailed descriptions to improve extraction accuracy
- Get confidence scores for extracted data using log probabilities
- **Optional reasoning explanations** - Control performance and costs with the `include_reasoning` flag
- Support for multiple field types (currently supports string fields)
- Easy integration with OpenAI API
- Similar functionality to RetellAI post-call processing

## Installation

```bash
pip install automatic-goggles
```

## Quick Start

```python
from transtype import TranscriptProcessor

# Initialize the processor with your OpenAI API key
processor = TranscriptProcessor(api_key="your-openai-api-key")

# Define your input data
data = {
    "messages": [
        {
            "role": "assistant",
            "content": "Hi, this is Marcus, I'm a customer service representative with TechFlow Solutions in Downtown Seattle."
        },
        {
            "role": "user", 
            "content": "I need to discuss my account billing issues."
        }
    ],
    "fields": [
        {
            "field_name": "representative_name",
            "field_type": "string",
            "format_example": "Sarah Chen",
            "field_description": "The name of the customer service representative or agent who is helping the customer. This should be extracted from their introduction or when they identify themselves during the conversation."
        }
    ]
}

# Process the transcript
result = processor.process(data)
print(result)
```

## Assertion Evaluation

Evaluate conversation quality against specific criteria using the `AssertsEvaluator` class:

```python
from transtype import AssertsEvaluator

# Initialize evaluator with evaluation steps
evaluator = AssertsEvaluator(
    api_key="your-openai-api-key",
    evaluation_steps=[
        "Did the agent ask for the caller's name?",
        "Did the agent offer to help the caller?",
        "Was the agent polite and professional?"
    ],
    threshold=0.7
)

# Evaluate conversation (supports both role/content and speaker/text formats)
conversation = {
    "messages": [
        {"role": "user", "content": "Hi, I need help with my account"},
        {"role": "assistant", "content": "Hello! I'd be happy to help. May I have your name?"}
    ]
}

result = evaluator.evaluate(conversation)
print(result)
# Output: {"result": {"score": 0.85, "success": True, "reason": "..."}}
```

## Field Definitions

Each field to be extracted must include the following properties:

- **`field_name`** (required): The name/identifier of the field to extract
- **`field_type`** (required): The data type of the field (currently only "string" is supported)  
- **`format_example`** (required): An example of the expected format for this field
- **`field_description`** (required): Detailed context and description to help the AI understand what to extract. The more specific and contextual this description is, the better the extraction accuracy will be.

> **Note**: Starting from version 2.0, `field_description` is a required field. If you're upgrading from an earlier version, you'll need to add descriptions to all your existing field definitions.

### Example Field Definition

```python
{
    "field_name": "customer_phone",
    "field_type": "string", 
    "format_example": "(555) 123-4567",
    "field_description": "The customer's phone number mentioned during the call. This could be their primary contact number, callback number, or the number they're calling about. Look for 10-digit phone numbers in various formats."
}
```

### Multiple Field Example

```python
data = {
    "messages": [
        {
            "role": "assistant",
            "content": "Hello, this is Sarah from TechSupport. How can I help you today?"
        },
        {
            "role": "user",
            "content": "Hi Sarah, I'm having issues with my account. My phone number is 555-123-4567 and my email is john.doe@example.com"
        }
    ],
    "fields": [
        {
            "field_name": "agent_name",
            "field_type": "string",
            "format_example": "Sarah Chen",
            "field_description": "The name of the customer service representative or support agent helping the customer. Usually mentioned in their introduction."
        },
        {
            "field_name": "customer_phone",
            "field_type": "string",
            "format_example": "(555) 123-4567",
            "field_description": "The customer's phone number mentioned during the conversation. Look for 10-digit numbers in formats like 555-123-4567, (555) 123-4567, or 5551234567."
        },
        {
            "field_name": "customer_email", 
            "field_type": "string",
            "format_example": "customer@example.com",
            "field_description": "The customer's email address provided during the call. Look for standard email format with @ symbol and domain."
        }
    ]
}
```

## Reasoning Flag

You can control whether to include reasoning explanations in the output using the `include_reasoning` parameter. This affects both performance and API costs:

### With Reasoning (Default)

```python
# Default behavior - includes detailed reasoning
processor = TranscriptProcessor(api_key="your-openai-api-key", include_reasoning=True)
# OR simply:
processor = TranscriptProcessor(api_key="your-openai-api-key")

result = processor.process(data)
# Output includes field_reason with explanation
```

### Without Reasoning (Faster & Cost-Effective)

```python
# Faster processing, lower API costs
processor = TranscriptProcessor(api_key="your-openai-api-key", include_reasoning=False)

result = processor.process(data)
# Output has field_reason set to null
```

**Benefits of disabling reasoning:**
- ⚡ **Faster processing** - Fewer tokens generated
- 💰 **Lower costs** - Reduced OpenAI API token usage
- 🎯 **Focused output** - Just the extracted values and confidence scores

**When to use each mode:**
- **With reasoning**: When you need explanations for debugging, quality assurance, or transparency
- **Without reasoning**: For production systems where you only need the extracted values

## Output Format

### With Reasoning (Default)

```json
{
    "fields": [
        {
            "field_name": "representative_name",
            "field_value": "Marcus",
            "field_confidence": 0.95,
            "field_reason": "Representative introduced himself as 'Marcus' at the beginning of the conversation"
        }
    ]
}
```

### Without Reasoning

```json
{
    "fields": [
        {
            "field_name": "representative_name",
            "field_value": "Marcus", 
            "field_confidence": 0.95,
            "field_reason": null
        }
    ]
}
```

## Requirements

- Python 3.8+
- OpenAI API key

## License

MIT License
