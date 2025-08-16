# Automatic Goggles

A Python package for extracting structured fields from call transcripts with confidence scores using DSPy and OpenAI's language models.

## Features

- Extract structured fields from conversation transcripts
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
            "format_example": "Sarah Chen"
        }
    ]
}

# Process the transcript
result = processor.process(data)
print(result)
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
