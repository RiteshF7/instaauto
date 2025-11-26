import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

from prompts import QUOTE_SYSTEM_PROMPT, SPACE_ENTITIES, CAPTION_SYSTEM_PROMPT

class QuoteService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=api_key)
            # Using gemini-2.5-flash as requested/supported
            self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_quote(self, prompt: str, description: str = "") -> str:
        """
        Generates a space fact. If prompt is 'random', picks a random entity.
        Otherwise uses the prompt as the entity.
        """
        try:
            entity = prompt.strip()
            if not entity or entity.lower() == "random":
                import random
                entity = random.choice(SPACE_ENTITIES)
            
            # Inject entity into system prompt template
            formatted_system_prompt = QUOTE_SYSTEM_PROMPT.replace("{{entity}}", entity)
            
            full_prompt = f"{formatted_system_prompt}\n\nContext: {description}" if description else formatted_system_prompt

            response = self.model.generate_content(full_prompt)
            cleaned_text = response.text.strip()
            if cleaned_text.lower().startswith("fun fact:"):
                cleaned_text = cleaned_text[9:].strip()
            return cleaned_text
        except Exception as e:
            print(f"Error generating fact: {e}")
            return "Space is vast and full of mysteries."

    def generate_caption(self, quote: str) -> str:
        """
        Generates an engaging Instagram caption for the quote.
        """
        try:
            prompt = CAPTION_SYSTEM_PROMPT.replace("{{quote}}", quote)
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating caption: {e}")
            return f"✨ {quote} ✨\n\n#space #universe #cosmos"
