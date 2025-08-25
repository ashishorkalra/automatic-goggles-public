"""
Example usage of the transtype package

This example demonstrates:
1. Basic field extraction with optional reasoning
2. Complex multi-field extraction including:
   - Names (agent and customer)
   - Contact information (phone and email)
   - Dates (incident, resolution, appointment dates)
   - Company information
3. Comprehensive field descriptions for better extraction accuracy
4. Processing with and without reasoning explanations
5. Summary reporting of extraction results

The complex example showcases real-world scenarios like insurance claims,
customer service calls, and appointment scheduling.
"""

import json
import os
from transtype import TranscriptProcessor


def main():
    # Get API key from environment variable or prompt user
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print("Or provide it when prompted.")
        api_key = input("Enter your OpenAI API key: ").strip()
        if not api_key:
            print("No API key provided. Exiting.")
            return

    # Example 1: Basic Example - With reasoning (default behavior)
    print("=== Example 1: Basic Example - With Reasoning (Default) ===")
    processor_with_reasoning = TranscriptProcessor(
        api_key=api_key, include_reasoning=True
    )

    # Example 2: Basic Example - Without reasoning
    print("\n=== Example 2: Basic Example - Without Reasoning ===")
    processor_without_reasoning = TranscriptProcessor(
        api_key=api_key, include_reasoning=False
    )

    # Basic example input data
    basic_input_data = {
        "messages": [
            {
                "role": "assistant",
                "content": "Hi, this is Marcus, I'm a customer service representative with TechFlow Solutions in Downtown Seattle. Our account manager is currently in a meeting, but I'm here to help with any questions. What can I assist you with today?",
            },
            {"role": "user", "content": "I need to discuss my account billing issues."},
            {
                "role": "assistant",
                "content": "I understand you have billing concerns. I can definitely help you with that. Let me pull up your account information. Can you please provide me with your account number or the email address associated with your account?",
            },
        ],
        "fields": [
            {
                "field_name": "representative_name",
                "field_type": "string",
                "format_example": "Sarah Chen",
                "field_description": "The name of the customer service representative or agent who is helping the customer. This should be extracted from their introduction or when they identify themselves during the conversation.",
            }
        ],
    }

    # Example 3: Complex Multi-Field Example
    print("\n=== Example 3: Complex Multi-Field Extraction ===")

    # Complex example with multiple field types
    complex_input_data = {
        "messages": [
            {
                "role": "assistant",
                "content": "Good morning! This is Sarah Johnson from Premium Insurance Services. I'm calling to follow up on your recent claim. How are you doing today?",
            },
            {
                "role": "user",
                "content": "Hi Sarah, I'm doing well. I've been waiting to hear back about my car insurance claim from the accident on March 15th, 2024.",
            },
            {
                "role": "assistant",
                "content": "I apologize for the delay. Let me pull up your file. Can you please confirm your contact information? I have your phone number as 555-123-4567 and email as john.smith@email.com. Is that correct?",
            },
            {
                "role": "user",
                "content": "Yes, that's correct. My phone is 555-123-4567 and email is john.smith@email.com. When do you think this will be resolved?",
            },
            {
                "role": "assistant",
                "content": "Thank you for confirming, Mr. Smith. Based on the adjuster's report, we should have this resolved by April 10th, 2024. You'll receive a check for the approved amount once everything is processed. Is there anything else I can help you with today?",
            },
            {
                "role": "user",
                "content": "That sounds good, Sarah. Just to confirm - my appointment with the adjuster is scheduled for March 25th, 2024 at 2:00 PM, right?",
            },
            {
                "role": "assistant",
                "content": "Let me check... Yes, that's correct. Your appointment with adjuster Mike Williams is confirmed for March 25th, 2024 at 2:00 PM. He'll meet you at the repair shop on Main Street.",
            },
        ],
        "fields": [
            {
                "field_name": "agent_name",
                "field_type": "string",
                "format_example": "Sarah Johnson",
                "field_description": "The full name of the insurance agent, customer service representative, or company employee who is assisting the customer. Look for introductions like 'This is [Name] from [Company]' or when they identify themselves during the conversation.",
            },
            {
                "field_name": "customer_name",
                "field_type": "string",
                "format_example": "John Smith",
                "field_description": "The customer's full name or last name. This could be mentioned when the agent addresses them (e.g., 'Mr. Smith', 'Ms. Johnson') or when the customer introduces themselves. Look for formal address patterns and name references.",
            },
            {
                "field_name": "customer_phone",
                "field_type": "string",
                "format_example": "(555) 123-4567",
                "field_description": "The customer's phone number mentioned during the call. This could be their primary contact number, callback number, or verification number. Look for 10-digit numbers in formats like 555-123-4567, (555) 123-4567, 555.123.4567, or 5551234567.",
            },
            {
                "field_name": "customer_email",
                "field_type": "string",
                "format_example": "customer@example.com",
                "field_description": "The customer's email address provided or confirmed during the conversation. Look for standard email format with @ symbol and domain (e.g., john@email.com, customer@company.org). This might be mentioned for verification or contact purposes.",
            },
            {
                "field_name": "incident_date",
                "field_type": "string",
                "format_example": "March 15, 2024",
                "field_description": "The date when the incident, accident, or event being discussed occurred. This could be mentioned as the claim date, accident date, or incident date. Look for dates in various formats like 'March 15, 2024', '03/15/2024', 'March 15th', or similar date references.",
            },
            {
                "field_name": "resolution_date",
                "field_type": "string",
                "format_example": "April 10, 2024",
                "field_description": "The expected or promised date when the issue, claim, or matter will be resolved or completed. This could be mentioned as 'resolved by', 'completed by', 'expected by', or similar future date references related to case resolution.",
            },
            {
                "field_name": "appointment_date",
                "field_type": "string",
                "format_example": "March 25, 2024",
                "field_description": "Any scheduled appointment date mentioned during the conversation. This could be for inspections, meetings, follow-ups, or other scheduled activities. Look for dates associated with 'appointment', 'meeting', 'scheduled', or 'visit'.",
            },
            {
                "field_name": "company_name",
                "field_type": "string",
                "format_example": "Premium Insurance Services",
                "field_description": "The name of the company, organization, or business that the agent represents. This is typically mentioned in the agent's introduction like 'calling from [Company Name]' or 'I'm with [Company Name]'.",
            },
        ],
    }

    try:
        # Process basic example with reasoning
        print("Processing basic example with reasoning...")
        result_with_reasoning = processor_with_reasoning.process(basic_input_data)
        print("Extraction Result (with reasoning):")
        print(json.dumps(result_with_reasoning, indent=2))

        # Process basic example without reasoning
        print("\nProcessing basic example without reasoning...")
        result_without_reasoning = processor_without_reasoning.process(basic_input_data)
        print("Extraction Result (without reasoning):")
        print(json.dumps(result_without_reasoning, indent=2))

        # Process complex example with reasoning
        print("\nProcessing complex multi-field example with reasoning...")
        complex_result = processor_with_reasoning.process(complex_input_data)
        print("Complex Extraction Result:")
        print(json.dumps(complex_result, indent=2))

        # Summary of extracted fields
        print("\n" + "=" * 60)
        print("EXTRACTION SUMMARY")
        print("=" * 60)

        print(
            f"\nBasic Example Fields Extracted: {len(result_with_reasoning['fields'])}"
        )
        for field in result_with_reasoning["fields"]:
            status = "✅ Found" if field["field_value"] else "❌ Not Found"
            confidence = f"({field['field_confidence']:.2f})"
            print(f"  {field['field_name']}: {status} {confidence}")

        print(f"\nComplex Example Fields Extracted: {len(complex_result['fields'])}")
        for field in complex_result["fields"]:
            status = "✅ Found" if field["field_value"] else "❌ Not Found"
            confidence = f"({field['field_confidence']:.2f})"
            value = (
                field["field_value"][:30] + "..."
                if field["field_value"] and len(field["field_value"]) > 30
                else field["field_value"]
            )
            print(f"  {field['field_name']}: {status} {confidence} - '{value}'")

        print("\n" + "=" * 60)
        print("All examples completed successfully!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
