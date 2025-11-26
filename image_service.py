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

    SYSTEM_PROMPT = "Create a cinematic, high-resolution, visually striking image that perfectly captures the mood of the text."

    def generate_image(self, quote: str) -> str:
        """
        Generates an image based on the quote using Gemini 2.5 Flash Image.
        Returns a base64 data URL.
        """
        if not self.client:
            return f"https://placehold.co/600x400?text={quote[:20]}..."

        try:
            prompt = f"{self.SYSTEM_PROMPT} Quote to visualize: '{quote}'. The image should be beautiful and suitable for social media."
            
            # Using the model and pattern provided by the user
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[prompt],
            )

            for part in response.parts:
                # Check for inline data (image)
                if part.inline_data is not None:
                    # Direct access to bytes from the SDK
                    img_bytes = part.inline_data.data
                    mime_type = part.inline_data.mime_type or "image/png"
                    
                    # Encode to base64
                    b64_str = base64.b64encode(img_bytes).decode('utf-8')
                    return f"data:{mime_type};base64,{b64_str}"
            
            print("No image data found in response.")
            return "https://placehold.co/600x400?text=No+Image+Generated"

        except Exception as e:
            print(f"Error generating image: {e}")
            return "https://placehold.co/600x400?text=Error+Generating+Image"
