# Transtype

A Python package for extracting structured fields from call transcripts with confidence scores using DSPy and OpenAI's language models.

## Features

- Extract structured fields from conversation transcripts
- Get confidence scores for extracted data using log probabilities
- Support for multiple field types (currently supports string fields)
- Easy integration with OpenAI API
- Similar functionality to RetellAI post-call processing

## Installation

```bash
pip install transtype
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
            "content": "Hi, this is Sophie, I'm a virtual assistant with CoJeer of Old Town, Alexandria."
        },
        {
            "role": "user", 
            "content": "I'd like to speak to the salesperson, not an assistant."
        }
    ],
    "fields": [
        {
            "field_name": "agent_name",
            "field_type": "string",
            "format_example": "John London"
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
            "field_name": "agent_name",
            "field_value": "Sophie",
            "field_confidence": 0.95,
            "field_reason": "Agent introduced herself as 'Sophie' at the beginning of the conversation"
        }
    ]
}
```

## Requirements

- Python 3.8+
- OpenAI API key

## License

MIT License
