"""
Tests for the transtype package
"""

from unittest.mock import MagicMock, Mock, patch

import pytest

from transtype import TranscriptInput, TranscriptProcessor
from transtype.models import FieldResult


class TestTranscriptProcessor:
    """Test cases for TranscriptProcessor"""

    @pytest.fixture
    def sample_fields(self):
        """Sample fields for testing"""
        return [
            {
                "field_name": "representative_name",
                "field_type": "string",
                "format_example": "Sarah Chen",
                "field_description": "The name of the customer service representative or agent who is helping the customer",
            }
        ]

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
        }

    @patch("transtype.processor.dspy")
    def test_processor_initialization(self, mock_dspy, sample_fields):
        """Test processor initialization"""
        mock_lm = MagicMock()
        mock_dspy.LM.return_value = mock_lm
        mock_dspy.settings.configure = MagicMock()
        mock_dspy.Predict = MagicMock()

        processor = TranscriptProcessor(api_key="test_key", fields=sample_fields)

        mock_dspy.LM.assert_called_once_with(
            "openai/gpt-4o", api_key="test_key", logprobs=True
        )
        mock_dspy.settings.configure.assert_called_once_with(lm=mock_lm)
        assert processor.include_reasoning is True
        assert processor.fields == sample_fields

    @patch("transtype.processor.dspy")
    def test_processor_initialization_no_reasoning(self, mock_dspy, sample_fields):
        """Test processor initialization without reasoning"""
        mock_lm = MagicMock()
        mock_dspy.LM.return_value = mock_lm
        mock_dspy.settings.configure = MagicMock()
        mock_dspy.Predict = MagicMock()

        processor = TranscriptProcessor(
            api_key="test_key", fields=sample_fields, include_reasoning=False
        )

        mock_dspy.LM.assert_called_once_with(
            "openai/gpt-4o", api_key="test_key", logprobs=True
        )
        mock_dspy.settings.configure.assert_called_once_with(lm=mock_lm)
        assert processor.include_reasoning is False
        assert processor.fields == sample_fields

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
        valid_data = {
            "messages": [{"role": "user", "content": "Hello"}],
        }
        validated = TranscriptInput(**valid_data)
        assert len(validated.messages) == 1

        with pytest.raises(Exception):
            TranscriptInput(messages=[{"role": "user"}])

    def test_confidence_calculation_no_logprobs(self):
        """Test confidence calculation when no logprobs available"""
        processor = TranscriptProcessor.__new__(TranscriptProcessor)
        confidence = processor._calculate_confidence_from_logprobs(None)
        assert confidence == 0.5

    def test_field_result_with_reasoning(self):
        """Test FieldResult model with reasoning"""
        result = FieldResult(
            field_name="test_field",
            field_value="test_value",
            field_confidence=0.95,
            field_reason="Test reasoning",
        )
        assert result.field_reason == "Test reasoning"

        # Test serialization
        data = result.model_dump()
        assert data["field_reason"] == "Test reasoning"

    def test_field_result_without_reasoning(self):
        """Test FieldResult model without reasoning"""
        result = FieldResult(
            field_name="test_field",
            field_value="test_value",
            field_confidence=0.95,
            field_reason=None,
        )
        assert result.field_reason is None

        # Test serialization
        data = result.model_dump()
        assert data["field_reason"] is None

    @patch("transtype.processor.dspy")
    def test_process_valid_input(self, mock_dspy, sample_fields, sample_input_data):
        """Test processing with valid input"""
        mock_lm = MagicMock()
        mock_dspy.LM.return_value = mock_lm
        mock_dspy.settings.configure = MagicMock()

        mock_result = Mock()
        mock_result.field_value = "Marcus"
        mock_result.reasoning = "Representative introduced himself as Marcus"
        mock_result.logprobs = None

        mock_predict_instance = MagicMock()
        mock_predict_instance.return_value = mock_result
        mock_dspy.Predict.return_value = mock_predict_instance

        processor = TranscriptProcessor(api_key="test_key", fields=sample_fields)
        result = processor.process(sample_input_data)

        assert "fields" in result
        assert len(result["fields"]) == 1
        assert result["fields"][0]["field_name"] == "representative_name"
        assert result["fields"][0]["field_value"] == "Marcus"
        assert result["fields"][0]["field_reason"] is not None

    @patch("transtype.processor.dspy")
    def test_process_without_reasoning(
        self, mock_dspy, sample_fields, sample_input_data
    ):
        """Test processing without reasoning"""
        mock_lm = MagicMock()
        mock_dspy.LM.return_value = mock_lm
        mock_dspy.settings.configure = MagicMock()

        mock_result = Mock()
        mock_result.field_value = "Marcus"
        mock_result.logprobs = None

        mock_predict_instance = MagicMock()
        mock_predict_instance.return_value = mock_result
        mock_dspy.Predict.return_value = mock_predict_instance

        processor = TranscriptProcessor(
            api_key="test_key", fields=sample_fields, include_reasoning=False
        )
        result = processor.process(sample_input_data)

        assert "fields" in result
        assert len(result["fields"]) == 1
        assert result["fields"][0]["field_name"] == "representative_name"
        assert result["fields"][0]["field_value"] == "Marcus"
        assert result["fields"][0]["field_reason"] is None


if __name__ == "__main__":
    pytest.main([__file__])
