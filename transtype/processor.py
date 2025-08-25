"""
Core processor for extracting fields from transcripts using DSPy
"""

import json
import math
from typing import Dict, Any
import dspy
from .models import TranscriptInput, TranscriptOutput, FieldResult


class FieldExtractionSignature(dspy.Signature):
    """Extract a specific field from a conversation transcript with confidence assessment."""

    transcript: str = dspy.InputField(desc="The full conversation transcript")
    field_name: str = dspy.InputField(desc="Name of the field to extract")
    field_type: str = dspy.InputField(desc="Type of the field to extract")
    format_example: str = dspy.InputField(desc="Example format for the field")
    field_description: str = dspy.InputField(
        desc="Context and description for the field"
    )

    field_value: str = dspy.OutputField(
        desc="The extracted value for the field, or 'NOT_FOUND' if not present"
    )
    reasoning: str = dspy.OutputField(
        desc="Detailed explanation of why this value was extracted or why it wasn't found"
    )


class FieldExtractionSignatureNoReasoning(dspy.Signature):
    """Extract a specific field from a conversation transcript without reasoning."""

    transcript: str = dspy.InputField(desc="The full conversation transcript")
    field_name: str = dspy.InputField(desc="Name of the field to extract")
    field_type: str = dspy.InputField(desc="Type of the field to extract")
    format_example: str = dspy.InputField(desc="Example format for the field")
    field_description: str = dspy.InputField(
        desc="Context and description for the field"
    )

    field_value: str = dspy.OutputField(
        desc="The extracted value for the field, or 'NOT_FOUND' if not present"
    )


class TranscriptProcessor:
    """Main processor class for extracting fields from transcripts"""

    def __init__(
        self, api_key: str, model: str = "gpt-4o", include_reasoning: bool = True
    ):
        """
        Initialize the transcript processor

        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o)
            include_reasoning: Whether to include reasoning in the output (default: True)
        """
        self.lm = dspy.LM(f"openai/{model}", api_key=api_key, logprobs=True)
        dspy.settings.configure(lm=self.lm)
        self.include_reasoning = include_reasoning

        # Initialize appropriate extractor based on reasoning requirement
        if include_reasoning:
            self.field_extractor = dspy.Predict(FieldExtractionSignature)
        else:
            self.field_extractor = dspy.Predict(FieldExtractionSignatureNoReasoning)

    def _format_transcript(self, messages: list) -> str:
        """Convert messages list to formatted transcript string"""
        transcript_parts = []
        for msg in messages:
            role_label = "Assistant" if msg["role"] == "assistant" else "User"
            transcript_parts.append(f"{role_label}: {msg['content']}")
        return "\n".join(transcript_parts)

    def _calculate_confidence_from_logprobs(self, logprobs_data) -> float:
        """
        Calculate confidence score from log probabilities

        Args:
            logprobs_data: Log probabilities data from the model response

        Returns:
            Confidence score between 0 and 1
        """
        if not logprobs_data or not hasattr(logprobs_data, "content"):
            return 0.5  # Default confidence if no logprobs available

        # Extract token logprobs and calculate average probability
        token_probs = []
        for token_logprob in logprobs_data.content:
            if hasattr(token_logprob, "logprob") and token_logprob.logprob is not None:
                # Convert log probability to probability
                prob = math.exp(token_logprob.logprob)
                token_probs.append(prob)

        if not token_probs:
            return 0.5

        # Calculate average probability and normalize
        avg_prob = sum(token_probs) / len(token_probs)

        # Apply sigmoid-like transformation to make confidence more meaningful
        # This helps distinguish between high and low confidence predictions
        confidence = min(max(avg_prob, 0.1), 0.99)

        return round(confidence, 3)

    def _extract_field(self, transcript: str, field_def: Dict[str, Any]) -> FieldResult:
        """
        Extract a single field from the transcript

        Args:
            transcript: Formatted conversation transcript
            field_def: Field definition dictionary

        Returns:
            FieldResult with extracted value and confidence
        """
        try:
            # Use DSPy to extract the field
            result = self.field_extractor(
                transcript=transcript,
                field_name=field_def["field_name"],
                field_type=field_def["field_type"],
                format_example=field_def["format_example"],
                field_description=field_def["field_description"],
            )

            # Extract the actual value and reasoning
            field_value = result.field_value.strip()
            reasoning = (
                result.reasoning.strip()
                if self.include_reasoning and hasattr(result, "reasoning")
                else None
            )

            # Check if field was found
            if field_value.upper() == "NOT_FOUND" or not field_value:
                field_value = None
                confidence = 0.1
            else:
                # Calculate confidence from logprobs
                confidence = self._calculate_confidence_from_logprobs(result.logprobs)

            return FieldResult(
                field_name=field_def["field_name"],
                field_value=field_value,
                field_confidence=confidence,
                field_reason=reasoning,
            )

        except Exception as e:
            # Handle any errors gracefully
            error_reason = (
                f"Error during extraction: {str(e)}" if self.include_reasoning else None
            )
            return FieldResult(
                field_name=field_def["field_name"],
                field_value=None,
                field_confidence=0.0,
                field_reason=error_reason,
            )

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process transcript and extract all specified fields

        Args:
            input_data: Dictionary containing messages and fields to extract

        Returns:
            Dictionary with extracted fields and confidence scores
        """
        # Validate input using Pydantic
        try:
            validated_input = TranscriptInput(**input_data)
        except Exception as e:
            raise ValueError(f"Invalid input format: {str(e)}")

        # Convert messages to transcript format
        transcript = self._format_transcript(
            [msg.model_dump() for msg in validated_input.messages]
        )

        # Extract each field
        field_results = []
        for field_def in validated_input.fields:
            field_result = self._extract_field(transcript, field_def.model_dump())
            field_results.append(field_result)

        # Create output
        output = TranscriptOutput(fields=field_results)
        return output.model_dump()

    def process_json(self, json_input: str) -> str:
        """
        Process JSON input and return JSON output

        Args:
            json_input: JSON string with transcript and field definitions

        Returns:
            JSON string with extraction results
        """
        try:
            input_data = json.loads(json_input)
            result = self.process(input_data)
            return json.dumps(result, indent=2)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON input: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Processing error: {str(e)}")
