"""
Tests for the transtype package
"""

import pytest
import json
from unittest.mock import Mock, patch
from transtype import TranscriptProcessor, TranscriptInput, FieldDefinition
from transtype.models import Message


class TestTranscriptProcessor:
    """Test cases for TranscriptProcessor"""

    @pytest.fixture
    def sample_input_data(self):
        """Sample input data for testing"""
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": "Hi, this is Marcus from TechFlow Solutions.",
                },
                {
                    "role": "user",
                    "content": "Hello Marcus, I need help with my billing.",
                },
            ],
            "fields": [
                {
                    "field_name": "representative_name",
                    "field_type": "string",
                    "format_example": "Sarah Chen",
                }
            ],
        }

    @patch("transtype.processor.dspy.LM")
    @patch("transtype.processor.dspy.settings.configure")
    def test_processor_initialization(self, mock_configure, mock_lm):
        """Test processor initialization"""
        processor = TranscriptProcessor(api_key="test_key")

        mock_lm.assert_called_once_with(
            "openai/gpt-4o", api_key="test_key", logprobs=True
        )
        mock_configure.assert_called_once()
        assert processor.include_reasoning is True  # Default value

    @patch("transtype.processor.dspy.LM")
    @patch("transtype.processor.dspy.settings.configure")
    def test_processor_initialization_no_reasoning(self, mock_configure, mock_lm):
        """Test processor initialization without reasoning"""
        processor = TranscriptProcessor(api_key="test_key", include_reasoning=False)

        mock_lm.assert_called_once_with(
            "openai/gpt-4o", api_key="test_key", logprobs=True
        )
        mock_configure.assert_called_once()
        assert processor.include_reasoning is False

    def test_format_transcript(self):
        """Test transcript formatting"""
        processor = TranscriptProcessor.__new__(TranscriptProcessor)
        messages = [
            {"role": "assistant", "content": "Hello"},
            {"role": "user", "content": "Hi there"},
        ]

        result = processor._format_transcript(messages)
        expected = "Assistant: Hello\nUser: Hi there"

        assert result == expected

    def test_input_validation(self):
        """Test input validation with Pydantic models"""
        # Valid input
        valid_data = {
            "messages": [{"role": "user", "content": "Hello"}],
            "fields": [
                {
                    "field_name": "test",
                    "field_type": "string",
                    "format_example": "example",
                }
            ],
        }
        validated = TranscriptInput(**valid_data)
        assert len(validated.messages) == 1
        assert len(validated.fields) == 1

        # Invalid input - missing required field
        with pytest.raises(Exception):
            TranscriptInput(messages=[{"role": "user"}])  # Missing content

    def test_confidence_calculation_no_logprobs(self):
        """Test confidence calculation when no logprobs available"""
        processor = TranscriptProcessor.__new__(TranscriptProcessor)
        confidence = processor._calculate_confidence_from_logprobs(None)
        assert confidence == 0.5

    @patch("transtype.processor.dspy.LM")
    @patch("transtype.processor.dspy.settings.configure")
    def test_process_valid_input(self, mock_configure, mock_lm, sample_input_data):
        """Test processing with valid input"""
        # Mock DSPy response
        mock_result = Mock()
        mock_result.field_value = "Marcus"
        mock_result.reasoning = "Representative introduced himself as Marcus"
        mock_result.logprobs = None

        with patch("transtype.processor.dspy.Predict") as mock_predict:
            mock_predict.return_value.return_value = mock_result

            processor = TranscriptProcessor(api_key="test_key")
            result = processor.process(sample_input_data)

            assert "fields" in result
            assert len(result["fields"]) == 1
            assert result["fields"][0]["field_name"] == "representative_name"
            assert result["fields"][0]["field_value"] == "Marcus"
            assert result["fields"][0]["field_reason"] is not None

    @patch("transtype.processor.dspy.LM")
    @patch("transtype.processor.dspy.settings.configure")
    def test_process_without_reasoning(
        self, mock_configure, mock_lm, sample_input_data
    ):
        """Test processing without reasoning"""
        # Mock DSPy response without reasoning
        mock_result = Mock()
        mock_result.field_value = "Marcus"
        mock_result.logprobs = None
        # No reasoning attribute when include_reasoning=False

        with patch("transtype.processor.dspy.Predict") as mock_predict:
            mock_predict.return_value.return_value = mock_result

            processor = TranscriptProcessor(api_key="test_key", include_reasoning=False)
            result = processor.process(sample_input_data)

            assert "fields" in result
            assert len(result["fields"]) == 1
            assert result["fields"][0]["field_name"] == "representative_name"
            assert result["fields"][0]["field_value"] == "Marcus"
            assert result["fields"][0]["field_reason"] is None


if __name__ == "__main__":
    pytest.main([__file__])
