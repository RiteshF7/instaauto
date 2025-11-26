#!/usr/bin/env python3
"""
Test script to verify Gemini Image Generation API
"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in environment variables.")
    exit(1)

print(f"OK: API Key found: {api_key[:10]}...")

try:
    client = genai.Client(api_key=api_key)
    print("OK: Client initialized successfully")
    
    # Test image generation with different models
    models_to_test = [
        "gemini-2.0-flash-exp-image-generation",
        "gemini-2.0-flash",
        "gemini-2.5-flash"
    ]
    
    test_prompt = "A beautiful cosmic scene with stars and nebula, vertical 9:16 aspect ratio, dark space background"
    
    for model_name in models_to_test:
        print(f"\n{'='*60}")
        print(f"Testing model: {model_name}")
        print(f"{'='*60}")
        print(f"Sending prompt: {test_prompt}")
        
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[test_prompt]
            )
            
            print(f"Response type: {type(response)}")
            
            # Check for image data
            has_image = False
            if hasattr(response, 'parts'):
                for i, part in enumerate(response.parts):
                    if hasattr(part, 'inline_data') and part.inline_data:
                        print(f"  Part {i}: Found inline_data! MIME: {part.inline_data.mime_type}, Size: {len(part.inline_data.data)} bytes")
                        has_image = True
                    elif hasattr(part, 'file_data') and part.file_data:
                        print(f"  Part {i}: Found file_data! URI: {part.file_data.file_uri}")
                        has_image = True
                    elif hasattr(part, 'text') and part.text:
                        print(f"  Part {i}: Has text (not image): {part.text[:80]}...")
            
            if has_image:
                print(f"SUCCESS: {model_name} generated an image!")
                break
            else:
                print(f"Model {model_name} did not return image data")
                
        except Exception as e:
            print(f"ERROR with {model_name}: {e}")
            import traceback
            traceback.print_exc()
        
        print()
    
    print(f"Response type: {type(response)}")
    print(f"Response attributes: {dir(response)}")
    
    if hasattr(response, 'parts'):
        print(f"Response has {len(response.parts)} parts")
        for i, part in enumerate(response.parts):
            print(f"\nPart {i}:")
            print(f"  Type: {type(part)}")
            
            # Check for inline_data
            if hasattr(part, 'inline_data'):
                inline_data = part.inline_data
                print(f"  inline_data: {inline_data}")
                if inline_data:
                    print(f"    MIME type: {inline_data.mime_type}")
                    if hasattr(inline_data, 'data'):
                        print(f"    Data length: {len(inline_data.data)} bytes")
            
            # Check for file_data
            if hasattr(part, 'file_data'):
                file_data = part.file_data
                print(f"  file_data: {file_data}")
                if file_data:
                    print(f"    MIME type: {file_data.mime_type}")
                    if hasattr(file_data, 'file_uri'):
                        print(f"    File URI: {file_data.file_uri}")
            
            # Check for as_image method
            if hasattr(part, 'as_image'):
                try:
                    img = part.as_image()
                    print(f"  as_image() returned: {type(img)}")
                except Exception as e:
                    print(f"  as_image() error: {e}")
            
            # Check for text
            if hasattr(part, 'text'):
                text = part.text
                if text:
                    print(f"  Has text: {text[:100]}...")
    else:
        print("Response does not have 'parts' attribute")
        print(f"Response: {response}")
    
    # Also check if response has direct image access
    if hasattr(response, 'candidates'):
        print(f"\nResponse candidates: {len(response.candidates) if response.candidates else 0}")
        if response.candidates:
            for i, candidate in enumerate(response.candidates):
                print(f"Candidate {i}: {type(candidate)}")
                if hasattr(candidate, 'content'):
                    print(f"  Content: {candidate.content}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

