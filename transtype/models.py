"""
Data models for transtype package using Pydantic
"""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Represents a single message in the conversation"""

    role: Literal["user", "assistant"] = Field(
        description="The role of the message sender"
    )
    content: str = Field(description="The content of the message")


class FieldDefinition(BaseModel):
    """Defines a field to be extracted from the transcript"""

    field_name: str = Field(description="Name of the field to extract")
    field_type: Literal["string"] = Field(
        description="Type of the field (currently only 'string' is supported)"
    )
    format_example: str = Field(
        description="Example of the expected format for this field"
    )
    field_description: str = Field(
        description="Context and description for the field to help with extraction"
    )


class TranscriptInput(BaseModel):
    """Input model for transcript processing"""

    messages: List[Message] = Field(description="List of messages in the conversation")
    fields: List[FieldDefinition] = Field(description="List of fields to extract")


class FieldResult(BaseModel):
    """Result for a single extracted field"""

    field_name: str = Field(description="Name of the extracted field")
    field_value: Optional[str] = Field(description="Extracted value for the field")
    field_confidence: float = Field(
        description="Confidence score between 0 and 1", ge=0, le=1
    )
    field_reason: Optional[str] = Field(
        default=None, description="Explanation for the extracted value (optional)"
    )


class TranscriptOutput(BaseModel):
    """Output model for transcript processing results"""

    fields: List[FieldResult] = Field(description="List of extracted field results")


class AssertionInput(BaseModel):
    """Input model for assertion evaluation"""

    messages: List[Message] = Field(description="List of messages in the conversation")


class AssertionResult(BaseModel):
    """Result for assertion evaluation"""

    score: float = Field(description="Evaluation score between 0 and 1", ge=0, le=1)
    confidence: float = Field(
        description="Confidence score between 0 and 1", ge=0, le=1
    )
    reason: Optional[str] = Field(
        default=None, description="Explanation for the evaluation score (optional)"
    )
    success: bool = Field(description="Whether the evaluation passed the threshold")


class AssertionOutput(BaseModel):
    """Output model for assertion evaluation results"""

    result: AssertionResult = Field(description="Assertion evaluation result")
