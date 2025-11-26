import os
from google import genai
from PIL import Image
import io
import base64
from dotenv import load_dotenv

load_dotenv(override=True)

class ImageService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not found.")
            self.client = None
        else:
            # Initialize the client with the API key
            self.client = genai.Client(api_key=self.api_key)

    SYSTEM_PROMPT = """You are a cosmic visual imagination agent. Your task is to generate a breathtaking space-themed image that directly reflects the meaning of the given quote, while also including the quote text inside the image.

Input:
Quote: "{{quote}}"

Instructions:
- Interpret the quote literally or metaphorically, and design a space scene that embodies its essence.
- Always use cosmic elements: galaxies, nebulae, planets, stars, black holes, or cosmic oceans.
- Integrate the quote text into the image:
  - Typography should match the mood (ethereal glow, cosmic shimmer, futuristic style).
  - Place the text harmoniously (e.g., floating among stars, glowing across a nebula, etched on a planet’s horizon).
  - Ensure readability against the background.
- The overall mood should evoke awe, mystery, and goosebumps.
- Style: cinematic, surreal, high-contrast, with deep cosmic colors (purples, blues, silvers, blacks).
- Format: Vertical aspect ratio (9:16) suitable for Instagram Reels.
- Do not invent random text — only include the provided quote.

Output format:
Image Prompt: [Detailed description of the cosmic scene that visually represents the quote + placement of the quote text + mention vertical 9:16 aspect ratio]
Progression Text: [A poetic 6–8 word phrase ending with ellipses]
Transparent Background: false"""

    def generate_image(self, quote: str) -> str:
        """
        Generates an image based on the quote using a two-step process:
        1. Generate a detailed image prompt using the Cosmic Agent persona (Text Model).
        2. Generate the actual image using the detailed prompt (Image Model).
        Returns a base64 data URL.
        """
        if not self.client:
            return f"https://placehold.co/600x400?text={quote[:20]}..."

        try:
            # Step 1: Generate the Image Prompt
            print(f"Generating image prompt for quote: {quote[:50]}...")
            text_prompt = self.SYSTEM_PROMPT.replace("{{quote}}", quote)
            
            text_response = self.client.models.generate_content(
                model="gemini-2.5-flash", # Use text model for prompt engineering
                contents=[text_prompt],
            )
            
            generated_prompt = text_response.text
            print(f"Generated Image Prompt: {generated_prompt[:100]}...")

            # Extract the "Image Prompt:" part if possible, or use the whole text
            final_image_prompt = generated_prompt
            if "Image Prompt:" in generated_prompt:
                final_image_prompt = generated_prompt.split("Image Prompt:")[1].split("Progression Text:")[0].strip()
            
            # Step 2: Generate the Image
            print(f"Generating image with prompt: {final_image_prompt[:50]}...")
            image_response = self.client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[final_image_prompt],
            )

            for part in image_response.parts:
                # Check for inline data (image)
                if part.inline_data is not None:
                    # Direct access to bytes from the SDK
                    img_bytes = part.inline_data.data
                    mime_type = part.inline_data.mime_type or "image/png"
                    
                    # Encode to base64
                    b64_str = base64.b64encode(img_bytes).decode('utf-8')
                    return f"data:{mime_type};base64,{b64_str}"
            
            # If we get here, check if there's text (error/refusal)
            if image_response.text:
                print(f"Image generation returned text instead of image: {image_response.text}")

            print("No image data found in response.")
            return "https://placehold.co/600x400?text=No+Image+Generated"

        except Exception as e:
            print(f"Error generating image: {e}")
            return "https://placehold.co/600x400?text=Error+Generating+Image"
