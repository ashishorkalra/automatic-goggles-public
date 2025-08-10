"""
Example usage of the transtype package
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
    
    processor = TranscriptProcessor(api_key=api_key)
    
    # Example input data
    input_data = {
        "messages": [
            {
                "role": "assistant",
                "content": "Hi, this is Marcus, I'm a customer service representative with TechFlow Solutions in Downtown Seattle. Our account manager is currently in a meeting, but I'm here to help with any questions. What can I assist you with today?"
            },
            {
                "role": "user",
                "content": "I need to discuss my account billing issues."
            },
            {
                "role": "assistant",
                "content": "I understand you have billing concerns. I can definitely help you with that. Let me pull up your account information. Can you please provide me with your account number or the email address associated with your account?"
            }
        ],
        "fields": [
            {
                "field_name": "representative_name",
                "field_type": "string",
                "format_example": "Sarah Chen"
            }
        ]
    }
    
    try:
        # Process the transcript
        result = processor.process(input_data)
        
        # Print the result
        print("Extraction Result:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
