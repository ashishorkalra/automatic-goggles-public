<div align="center">

<img src="docs/resources/image.png" alt="Automatic Goggles Logo" width="200"/>

# Automatic Goggles

[![PyPI version](https://badge.fury.io/py/automatic-goggles.svg)](https://badge.fury.io/py/automatic-goggles)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/automatic-goggles)](https://pepy.tech/project/automatic-goggles)

**Post-Call Analysis & Conversational Evaluation**

*Extract structured fields from transcripts with confidence scores and evaluate conversation quality using Assertive LLM-as-a-Judge*

[Automatic-Goggles?](#-what-is-automatic-goggles) | [Installation](#-installation) | [Quick Start](#-examples) | [Features](#-features) | [Use-Cases](#-use-cases)

</div>

---

## 🎯 What is Automatic Goggles?

**Automatic Goggles** is a lightweight, production-ready Python package for analyzing conversation transcripts. It provides two core capabilities:

1. **🔍 Field Extraction** - Extract structured data (names, emails, dates, custom fields) from transcripts with confidence scores
2. **⚖️ Conversation Evaluation** - Assess conversation quality against custom assertions using LLM-as-a-Judge

Built for **voice agent post-call analysis**, customer support quality assurance, and conversational AI evaluation.

---
[Go to Installation](#installation)
## 🚀 Installation

```bash
pip install automatic-goggles
```

Requires Python 3.8+

## 🚀 Examples

### Field Extraction in 30 Seconds

```python
from transtype import TranscriptProcessor

fields = [
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

processor = TranscriptProcessor(
    api_key="your-openai-api-key",
    fields=fields,
    include_reasoning=True
)

conversation = {
    "messages": [
        {"role": "assistant", "content": "My name is Sarah Chen, you can reach me at sarah@example.com"},
        {"role": "user", "content": "Thanks, I'll email you"}
    ]
}

result = processor.process(conversation)
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

### Conversation Evaluation in 30 Seconds

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
- ✅ **Weighted Scoring** - Confidence-weighted scores
- ✅ **Pass/Fail Thresholds** - Configurable success criteria
- ✅ **Multi-Turn Support** - Evaluate entire conversations

### Technical Highlights
- ⚡ **Fast & Cost-Effective** - Optional reasoning for performance tuning
- 🧪 **Production-Ready** - Confidence scores for reliability filtering
- 📊 **Transparent** - Get reasoning explanations for every extraction/evaluation

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
- **Email**: ashishorkalra@gmail.com
- **Package**: [PyPI - automatic-goggles](https://pypi.org/project/automatic-goggles/)

---

<div align="center">

**Built with ❤️ by developers, for developers**

[⭐ Star on GitHub](https://github.com/ashishorkalra/automatic-goggles-public) | [📦 Install Now](https://pypi.org/project/automatic-goggles/)

</div>
