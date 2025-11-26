#!/usr/bin/env python3
"""
Test script to verify Gemini API connection and model usage
"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in environment variables.")
    print("Please create a .env file with: GEMINI_API_KEY=your_api_key_here")
    exit(1)

print(f"OK: API Key found: {api_key[:10]}...")

try:
    client = genai.Client(api_key=api_key)
    print("OK: Client initialized successfully")
    
    # Test quote generation
    print("\nTesting quote generation with gemini-2.5-flash...")
    test_prompt = "You are a space educator bot. Generate a fun fact about the Moon. Keep it short and engaging."
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[test_prompt]
    )
    
    if response and hasattr(response, 'text'):
        print("OK: Quote generated successfully!")
        try:
            print(f"Response: {response.text[:100]}...")
        except UnicodeEncodeError:
            print("Response: [Contains special characters - API working correctly]")
    else:
        print("ERROR: Invalid response from API")
        print(f"Response object: {response}")
        print(f"Response type: {type(response)}")
        print(f"Response dir: {dir(response)}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

