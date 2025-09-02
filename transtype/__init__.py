"""
Transtype - A package for extracting structured fields from call transcripts with confidence scores
"""

from .processor import TranscriptProcessor
from .models import TranscriptInput, FieldDefinition, FieldResult, TranscriptOutput

__version__ = "0.4.0"
__all__ = [
    "TranscriptProcessor",
    "TranscriptInput",
    "FieldDefinition",
    "FieldResult",
    "TranscriptOutput",
]
