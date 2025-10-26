"""
Transtype - A package for extracting structured fields from call transcripts with confidence scores
"""

from .models import (
    AssertionInput,
    AssertionOutput,
    AssertionResult,
    FieldDefinition,
    FieldResult,
    TranscriptInput,
    TranscriptOutput,
)
from .processor import AssertsEvaluator, TranscriptProcessor

__version__ = "0.7.0"
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
