import os
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)

from prompts import QUOTE_SYSTEM_PROMPT, SPACE_ENTITIES, CAPTION_SYSTEM_PROMPT

class QuoteService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("ERROR: GEMINI_API_KEY not found in environment variables.")
            print("Please set GEMINI_API_KEY in your .env file or environment variables.")
            self.client = None
        else:
            try:
                # Initialize the client with the API key
                self.client = genai.Client(api_key=self.api_key)
                print("✅ QuoteService initialized successfully with API key")
            except Exception as e:
                print(f"ERROR: Failed to initialize Gemini client: {e}")
                self.client = None

    def generate_quote(self, prompt: str, description: str = "") -> str:
        """
        Generates a space fact. If prompt is 'random', picks a random entity.
        Otherwise uses the prompt as the entity.
        """
        if not self.client:
            print("ERROR: GEMINI_API_KEY not found. Cannot generate quote.")
            return "Space is vast and full of mysteries."
        
        try:
            entity = prompt.strip()
            if not entity or entity.lower() == "random":
                import random
                entity = random.choice(SPACE_ENTITIES)
            
            # Inject entity into system prompt template
            formatted_system_prompt = QUOTE_SYSTEM_PROMPT.replace("{{entity}}", entity)
            
            full_prompt = f"{formatted_system_prompt}\n\nContext: {description}" if description else formatted_system_prompt

            print(f"Generating quote for entity: {entity}")
            print(f"Using model: gemini-2.5-flash")
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[full_prompt]
            )
            
            if not response or not hasattr(response, 'text'):
                print("ERROR: Invalid response from API")
                return "Space is vast and full of mysteries."
            
            cleaned_text = response.text.strip()
            if cleaned_text.lower().startswith("fun fact:"):
                cleaned_text = cleaned_text[9:].strip()
            print(f"Generated quote: {cleaned_text[:50]}...")
            return cleaned_text
        except Exception as e:
            print(f"Error generating fact: {e}")
            import traceback
            traceback.print_exc()
            return "Space is vast and full of mysteries."

    def generate_caption(self, quote: str) -> str:
        """
        Generates an engaging Instagram caption for the quote.
        """
        if not self.client:
            return f"✨ {quote} ✨\n\n#space #universe #cosmos"
        
        try:
            prompt = CAPTION_SYSTEM_PROMPT.replace("{{quote}}", quote)
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt]
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error generating caption: {e}")
            return f"✨ {quote} ✨\n\n#space #universe #cosmos"
