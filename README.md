# Automatic Goggles

<div align="center">

[![PyPI version](https://badge.fury.io/py/automatic-goggles.svg)](https://badge.fury.io/py/automatic-goggles)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/automatic-goggles)](https://pepy.tech/project/automatic-goggles)

**Post-Call Analysis & Conversational Evaluation**

*Extract structured fields from transcripts with confidence scores and evaluate conversation quality using Assertive LLM-as-a-Judge*

[Documentation](#documentation) | [Installation](#installation) | [Quick Start](#examples) | [Features](#features) | [Examples](#examples)

</div>

---

## 🎯 What is Automatic Goggles?

**Automatic Goggles** is a lightweight, production-ready Python package for analyzing conversation transcripts. It provides two core capabilities:

1. **🔍 Field Extraction** - Extract structured data (names, emails, dates, custom fields) from transcripts with confidence scores
2. **⚖️ Conversation Evaluation** - Assess conversation quality against custom assertions using LLM-as-a-Judge

Built for **voice agent post-call analysis**, customer support quality assurance, and conversational AI evaluation.

---

## 🚀 Installation

```bash
pip install automatic-goggles
```

Requires Python 3.8+

## 🚀 Examples

### Field Extraction in 30 Seconds

```python
from transtype import TranscriptProcessor

# Initialize with your OpenAI API key
processor = TranscriptProcessor(api_key="your-openai-api-key")

# Define conversation and fields to extract
data = {
    "messages": [
        {"role": "assistant", "content": "Hi, this is Marcus from TechFlow Solutions."},
        {"role": "user", "content": "I need help with my account."}
    ],
    "fields": [
        {
            "field_name": "representative_name",
            "field_type": "string",
            "format_example": "Sarah Chen",
            "field_description": "Name of the customer service representative"
        }
    ]
}

# Extract fields
result = processor.process(data)
print(result)
# Output: {'fields': [{'field_name': 'representative_name', 'field_value': 'Marcus', 
#                      'field_confidence': 0.95, 'field_reason': '...'}]}
```

### Conversation Evaluation in 30 Seconds

```python
from transtype import AssertsEvaluator

# Initialize with evaluation criteria
evaluator = AssertsEvaluator(
    api_key="your-openai-api-key",
    evaluation_steps=[
        "Did the agent ask for the caller's name?",
        "Was the agent polite and professional?"
    ],
    threshold=0.7
)

# Evaluate conversation
conversation = {
    "messages": [
        {"role": "user", "content": "Hi, I need help"},
        {"role": "assistant", "content": "Hello! I'd be happy to help. May I have your name?"}
    ]
}

result = evaluator.evaluate(conversation)
print(result)
# Output: {"result": {"score": 0.85, "success": True, "reason": "..."}}
```

---

## 🔥 Features

### Field Extraction
- ✅ **Confidence-Weighted Scoring** - Log probability-based confidence scores (0-1)
- ✅ **Contextual Descriptions** - Improve accuracy with detailed field descriptions
- ✅ **Flexible Reasoning** - Toggle explanations on/off for performance/cost optimization
- ✅ **Multi-Field Support** - Extract multiple fields in one pass
- ✅ **Format Examples** - Guide extraction with format examples

### Conversation Evaluation
- ✅ **LLM-as-a-Judge** - Research-backed evaluation using GPT models
- ✅ **Custom Assertions** - Define your own quality criteria
- ✅ **Weighted Scoring** - Confidence-weighted scores inspired by [DeepEval's ConversationalGEval](https://github.com/confident-ai/deepeval)
- ✅ **Pass/Fail Thresholds** - Configurable success criteria
- ✅ **Multi-Turn Support** - Evaluate entire conversations

### Technical Highlights
- 🔧 Built on **DSPy** for robust LLM orchestration
- ⚡ **Fast & Cost-Effective** - Optional reasoning for performance tuning
- 🧪 **Production-Ready** - Confidence scores for reliability filtering
- 📊 **Transparent** - Get reasoning explanations for every extraction/evaluation

---

## 📦 What's New in v0.6.0

### Enhanced Confidence-Weighted Scoring

- **Added confidence field** to evaluation results for transparency
- **Implemented weighted score calculation** using log probabilities (inspired by [DeepEval's ConversationalGEval](https://github.com/confident-ai/deepeval))
- **More nuanced results** - Scores reflect model certainty

---

## 📚 Core Concepts

### 1. Field Extraction

Extract structured data from unstructured conversations:

```python
from transtype import TranscriptProcessor

processor = TranscriptProcessor(
    api_key="your-openai-api-key",
    include_reasoning=True  # Set False for faster/cheaper processing
)

data = {
    "messages": [
        {"role": "assistant", "content": "My name is Sarah Chen, you can reach me at sarah@example.com"},
        {"role": "user", "content": "Thanks, I'll email you"}
    ],
    "fields": [
        {
            "field_name": "agent_email",
            "field_type": "string",
            "format_example": "agent@company.com",
            "field_description": "The agent's email address for follow-up communication"
        },
        {
            "field_name": "agent_name",
            "field_type": "string",
            "format_example": "John Doe",
            "field_description": "Full name of the customer service agent"
        }
    ]
}

result = processor.process(data)
```

**Output:**
```json
{
    "fields": [
        {
            "field_name": "agent_email",
            "field_value": "sarah@example.com",
            "field_confidence": 0.92,
            "field_reason": "Email explicitly mentioned by agent"
        },
        {
            "field_name": "agent_name",
            "field_value": "Sarah Chen",
            "field_confidence": 0.95,
            "field_reason": "Agent introduced herself by name"
        }
    ]
}
```

### 2. Conversation Evaluation

Assess conversation quality against custom criteria:

```python
from transtype import AssertsEvaluator

evaluator = AssertsEvaluator(
    api_key="your-openai-api-key",
    evaluation_steps=[
        "Did the agent greet the customer politely?",
        "Did the agent ask clarifying questions?",
        "Did the agent resolve the customer's issue?",
        "Did the agent offer additional help?"
    ],
    threshold=0.7  # Pass threshold (0-1)
)

conversation = {
    "messages": [
        {"role": "user", "content": "My internet isn't working"},
        {"role": "assistant", "content": "Good morning! I'm sorry to hear that. When did this issue start?"},
        {"role": "user", "content": "This morning"},
        {"role": "assistant", "content": "Let me help you troubleshoot. Can you check if your router is powered on?"}
    ]
}

result = evaluator.evaluate(conversation)
```

**Output:**
```json
{
    "result": {
        "score": 0.88,
        "success": true,
        "reason": "Agent demonstrated professionalism, asked clarifying questions, and initiated troubleshooting"
    }
}
```

---

## 🎓 Advanced Usage

### Controlling Reasoning Output

**With Reasoning (Default)**
```python
processor = TranscriptProcessor(api_key="...", include_reasoning=True)
# Benefits: Transparency, debugging, quality assurance
# Trade-offs: Slightly slower, higher token costs
```

**Without Reasoning (Production-Optimized)**
```python
processor = TranscriptProcessor(api_key="...", include_reasoning=False)
# Benefits: ⚡ Faster processing, 💰 Lower costs
# Trade-offs: No explanation for extracted values
```

### Handling Multiple Conversation Formats

Automatic Goggles supports both formats:

```python
# Format 1: role/content (OpenAI-style)
conversation_1 = {
    "messages": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
}

# Format 2: speaker/text (transcript-style)
conversation_2 = {
    "messages": [
        {"speaker": "customer", "text": "Hello"},
        {"speaker": "agent", "text": "Hi there!"}
    ]
}

# Both work seamlessly
evaluator.evaluate(conversation_1)
evaluator.evaluate(conversation_2)
```

---

## 💡 Use Cases

| Use Case | Description |
|----------|-------------|
| **Voice Agent Post-Call Analysis** | Extract key information (phone numbers, appointment dates, action items) after customer calls |
| **Quality Assurance** | Evaluate if agents followed scripts, were polite, and resolved issues |
| **Compliance Monitoring** | Verify agents disclosed required information (privacy policies, terms) |
| **Training & Coaching** | Identify coaching opportunities by evaluating agent performance against best practices |
| **Customer Insights** | Extract sentiment, pain points, and feature requests from support transcripts |

---

## 🛠️ Field Definition Schema

Each field requires:

| Property | Required | Description |
|----------|----------|-------------|
| `field_name` | ✅ Yes | Unique identifier for the field |
| `field_type` | ✅ Yes | Data type (currently supports `"string"`) |
| `format_example` | ✅ Yes | Example of expected format (e.g., `"(555) 123-4567"`) |
| `field_description` | ✅ Yes | Detailed context to guide extraction accuracy |

**Example:**
```python
{
    "field_name": "customer_phone",
    "field_type": "string",
    "format_example": "(555) 123-4567",
    "field_description": "The customer's primary phone number for callbacks. Look for 10-digit numbers in various formats."
}
```

---

## 🔄 Comparison with Similar Tools

| Feature | Automatic Goggles | RetellAI | DeepEval |
|---------|-------------------|----------|----------|
| **Field Extraction** | ✅ Core feature | ✅ Yes | ❌ No |
| **Conversation Evaluation** | ✅ LLM-as-a-Judge | ❌ No | ✅ Yes |
| **Confidence Scores** | ✅ Log probability-based | ⚠️ Limited | ✅ Yes |
| **Contextual Descriptions** | ✅ Required | ⚠️ Optional | N/A |
| **Custom Assertions** | ✅ Flexible | ❌ No | ✅ Yes |
| **Open Source** | ✅ MIT License | ❌ No | ✅ Apache 2.0 |

---

## 📖 Documentation

### TranscriptProcessor API

```python
processor = TranscriptProcessor(
    api_key: str,              # OpenAI API key
    include_reasoning: bool = True  # Include explanations in output
)

result = processor.process(data: dict)
# data: {"messages": [...], "fields": [...]}
# returns: {"fields": [{"field_name": str, "field_value": str, 
#                       "field_confidence": float, "field_reason": str}]}
```

### AssertsEvaluator API

```python
evaluator = AssertsEvaluator(
    api_key: str,                    # OpenAI API key
    evaluation_steps: List[str],     # List of assertions to evaluate
    threshold: float = 0.7           # Pass/fail threshold (0-1)
)

result = evaluator.evaluate(conversation: dict)
# conversation: {"messages": [...]}
# returns: {"result": {"score": float, "success": bool, "reason": str}}
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs** - Open an issue on [GitHub](https://github.com/ashishorkalra/automatic-goggles-public/issues)
2. **Feature Requests** - Suggest new features via issues
3. **Pull Requests** - Submit PRs for bug fixes or features
4. **Documentation** - Improve docs or add examples

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- Inspired by [DeepEval's ConversationalGEval](https://github.com/confident-ai/deepeval) for confidence-weighted scoring
- Built with [DSPy](https://github.com/stanfordnlp/dspy) for robust LLM orchestration
- Powered by [OpenAI](https://openai.com/) language models

---

## 📬 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/ashishorkalra/automatic-goggles-public/issues)
- **Email**: ashish@talkfurther.com
- **Package**: [PyPI - automatic-goggles](https://pypi.org/project/automatic-goggles/)

---

<div align="center">

**Built with ❤️ by developers, for developers**

[⭐ Star on GitHub](https://github.com/ashishorkalra/automatic-goggles-public) | [📦 Install Now](https://pypi.org/project/automatic-goggles/)

</div>
