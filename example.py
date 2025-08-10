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
                "content": "Hi, this is Sophie, I'm a virtual assistant with CoJeer of Old Town, Alexandria. Our sales director is currently unavailable, but I am happy to answer any questions. Can you please tell me why you are calling, today?"
            },
            {
                "role": "user",
                "content": "I'd like to speak to the salesperson, not an assistant."
            },
            {
                "role": "assistant",
                "content": "I understand you'd prefer to speak with a salesperson directly. I can help connect you with a team member. Would you like me to take your contact details so they can call you back, or would you prefer I escalate this for immediate assistance?"
            }
        ],
        "fields": [
            {
                "field_name": "agent_name",
                "field_type": "string",
                "format_example": "John London"
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
