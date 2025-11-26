import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

class QuoteService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=api_key)
            # Using gemini-2.5-flash as requested/supported
            self.model = genai.GenerativeModel('gemini-2.5-flash')

    SYSTEM_PROMPT = "You are a wise and eloquent assistant specialized in generating impactful, short, and inspirational quotes."

    def generate_quote(self, prompt: str, description: str = "") -> str:
        """
        Generates a short, inspirational quote based on the prompt and description.
        """
        try:
            full_prompt = f"{self.SYSTEM_PROMPT}\n\nUser Request: Generate a short, inspirational quote (1-2 sentences) based on this topic: '{prompt}'. "
            if description:
                full_prompt += f"Context: {description}. "
            full_prompt += "Return ONLY the quote, no extra text or quotation marks."

            response = self.model.generate_content(full_prompt)
            return response.text.strip().strip('"')
        except Exception as e:
            print(f"Error generating quote: {e}")
            return "Failure is not the opposite of success; it's part of success." # Fallback quote
