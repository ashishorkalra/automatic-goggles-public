# Automatic Goggles

A Python package for extracting structured fields from call transcripts with confidence scores using DSPy and OpenAI's language models.

## Features

- Extract structured fields from conversation transcripts
- Get confidence scores for extracted data using log probabilities
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

## Output Format

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

## Requirements

- Python 3.8+
- OpenAI API key

## License

MIT License
