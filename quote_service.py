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

    SYSTEM_PROMPT = """You are a space educator bot. Your task is to generate a single fun fact about the following celestial object:

**Entity**: {{entity}}

Guidelines:
- Keep the fact short (1–3 sentences).
- Make it surprising, quirky, or awe-inspiring.
- Avoid technical jargon unless it's explained simply.
- Do not repeat facts already widely known (e.g., “The Sun is hot”).

Output format:
Fun Fact: [Your fact here]"""

    SPACE_ENTITIES = [
        "Moon", "Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune",
        "Pluto", "Ceres", "Eris", "Haumea", "Makemake",  # Dwarf planets
        "Asteroids", "Comets", "Meteorites",
        "Milky Way", "Andromeda", "Sombrero Galaxy", "Whirlpool Galaxy",
        "Black Holes", "Neutron Stars", "Pulsars", "Quasars",
        "Alpha Centauri", "Betelgeuse", "Sirius", "Polaris", "Vega",  # Stars
        "Orion Nebula", "Crab Nebula", "Carina Nebula",
        "Exoplanets", "Star Clusters", "Cosmic Microwave Background"
    ]

    def generate_quote(self, prompt: str, description: str = "") -> str:
        """
        Generates a space fact. If prompt is 'random', picks a random entity.
        Otherwise uses the prompt as the entity.
        """
        try:
            entity = prompt.strip()
            if not entity or entity.lower() == "random":
                import random
                entity = random.choice(self.SPACE_ENTITIES)
            
            # Inject entity into system prompt template
            formatted_system_prompt = self.SYSTEM_PROMPT.replace("{{entity}}", entity)
            
            full_prompt = f"{formatted_system_prompt}\n\nContext: {description}" if description else formatted_system_prompt

            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating fact: {e}")
            return "Space is vast and full of mysteries."

    def generate_caption(self, quote: str) -> str:
        """
        Generates an engaging Instagram caption for the quote.
        """
        try:
            prompt = f"""You are a social media expert. Generate an engaging Instagram caption for this quote/fact:
"{quote}"

Requirements:
- Start with a hook or emoji.
- Include the quote/fact naturally if needed, or just comment on it.
- Add 15-20 relevant, high-reach hashtags (e.g., #space, #universe, #astronomy, #cosmos, etc.).
- Keep it clean and spaced out.

Output ONLY the caption text."""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating caption: {e}")
            return f"✨ {quote} ✨\n\n#space #universe #cosmos"
