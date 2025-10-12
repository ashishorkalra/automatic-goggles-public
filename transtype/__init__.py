"""
Transtype - A package for extracting structured fields from call transcripts with confidence scores
"""

from .processor import TranscriptProcessor, AssertsEvaluator
from .models import (
    TranscriptInput,
    FieldDefinition,
    FieldResult,
    TranscriptOutput,
    AssertionInput,
    AssertionResult,
    AssertionOutput,
)

__version__ = "0.5.0"
__all__ = [
    "TranscriptProcessor",
    "AssertsEvaluator",
    "TranscriptInput",
    "FieldDefinition",
    "FieldResult",
    "TranscriptOutput",
    "AssertionInput",
    "AssertionResult",
    "AssertionOutput",
]
