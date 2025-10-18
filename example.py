"""
Example usage of the transtype package

This example demonstrates:
1. Basic field extraction with optional reasoning
2. Complex multi-field extraction including:
   - Names (agent and customer)
   - Contact information (phone and email - with updates)
   - Dates (incident, resolution, and relative appointment dates)
   - Company information
3. Relative date calculation for appointments (next Friday from incident date)
4. Comprehensive field descriptions for better extraction accuracy
5. Processing with and without reasoning explanations
6. Summary reporting of extraction results

The complex example showcases real-world scenarios like insurance claims,
customer service calls, and appointment scheduling with relative date logic.
The appointment date demonstrates calculating "next Friday" relative to an
incident date, simulating realistic business scheduling patterns.
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

    # Complex example with multiple field types and relative date functionality
    complex_input_data = {
        "messages": [
            {
                "role": "assistant",
                "content": "Good morning! This is Joan London from ABC Insurance Solutions. I'm calling regarding your recent vehicle damage claim. How are you today?",
            },
            {
                "role": "user",
                "content": "Hi Joan, I'm doing okay considering the circumstances. I submitted the claim for the accident that happened on August 11th, 2025.",
            },
            {
                "role": "assistant",
                "content": "I understand, and I'm sorry to hear about your accident. Let me pull up your claim details. Can you verify your contact information? I show your phone as 217-218-1234 and your email as will.tis@gmail.com. Is this still current?",
            },
            {
                "role": "user",
                "content": "Actually, my phone number has changed. It's now 217-918-2344, but the email address will.tis@gmail.com is correct.",
            },
            {
                "role": "assistant",
                "content": "Perfect, I've updated your phone to 217-918-2344. Thank you, Mr. Tesco. Now, regarding the resolution timeline, we expect to have everything finalized by January 15th, 2026. However, we do need to schedule an inspection appointment.",
            },
            {
                "role": "user",
                "content": "When would that inspection be? I hope it's soon so we can get this moving.",
            },
            {
                "role": "assistant",
                "content": "Absolutely! Since the accident was on August 11th, yesterday, we always schedule inspections for the Friday of the following week. So your appointment will be next week Friday from the incident date. Let me see... that would be perfect for our inspector's schedule.",
            },
            {
                "role": "user",
                "content": "So just to confirm - the appointment is the next week Friday after August 11 2025? And will this be with the same adjuster who handled my previous claim?",
            },
            {
                "role": "assistant",
                "content": "That's correct - next week Friday after the incident date. And no, this will be with our specialist David Chen, not the previous adjuster. He'll meet you at the collision center on Oak Avenue at 10:30 AM.",
            },
        ],
        "fields": [
            {
                "field_name": "agent_name",
                "field_type": "string",
                "format_example": "Jennifer Martinez",
                "field_description": "The full name of the insurance agent, customer service representative, or company employee who is assisting the customer. Look for introductions like 'This is [Name] from [Company]' or when they identify themselves during the conversation.",
            },
            {
                "field_name": "customer_name",
                "field_type": "string",
                "format_example": "Michael Torres",
                "field_description": "The customer's full name or last name. This could be mentioned when the agent addresses them (e.g., 'Mr. Torres', 'Ms. Johnson') or when the customer introduces themselves. Look for formal address patterns and name references.",
            },
            {
                "field_name": "customer_phone",
                "field_type": "string",
                "format_example": "415-555-9876",
                "field_description": "The customer's current phone number mentioned during the call. Pay attention to any updates or corrections to phone numbers during the conversation. Look for 10-digit numbers in formats like 415-555-9876, (415) 555-9876, or similar patterns.",
            },
            {
                "field_name": "customer_email",
                "field_type": "string",
                "format_example": "michael.torres@techcorp.com",
                "field_description": "The customer's email address provided or confirmed during the conversation. Look for standard email format with @ symbol and domain. This might be mentioned for verification or contact purposes.",
            },
            {
                "field_name": "incident_date",
                "field_type": "string",
                "format_example": "December 8, 2024",
                "field_description": "The exact date when the incident, accident, or event being discussed occurred. This is the base date for calculating other related dates. Look for dates mentioned as 'accident date', 'incident date', or when the event happened.",
            },
            {
                "field_name": "resolution_date",
                "field_type": "string",
                "format_example": "January 15, 2024",
                "field_description": "The expected or promised date when the issue, claim, or matter will be resolved or completed. This could be mentioned as 'resolved by', 'completed by', 'finalized by', or similar future date references related to case resolution.",
            },
            {
                "field_name": "appointment_date",
                "field_type": "string",
                "format_example": "December 13, 2024",
                "field_description": "The calculated appointment date that is always scheduled for 'next Friday' relative to the incident date. When the conversation mentions 'next week Friday after the incident date' or 'Friday of the following week from the accident', calculate the actual date. For incident on December 3, 2024 (Tuesday), next week Friday would be December 13, 2024.",
            },
            {
                "field_name": "company_name",
                "field_type": "string",
                "format_example": "AutoClaim Solutions",
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
