"""
Image Generation Service
Handles AI-powered image generation using Gemini API.
"""
import os
from google import genai
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv(override=True)

from prompts import IMAGE_SYSTEM_PROMPT

class ImageService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("ERROR: GEMINI_API_KEY not found.")
            print("Please set GEMINI_API_KEY in your .env file or environment variables.")
            self.client = None
        else:
            try:
                # Initialize the client with the API key
                self.client = genai.Client(api_key=self.api_key)
                print("OK: ImageService initialized successfully with API key")
            except Exception as e:
                print(f"ERROR: Failed to initialize Gemini client: {e}")
                self.client = None

    def generate_image(self, quote: str) -> Image.Image:
        """
        Generates an image based on the quote using Gemini image generation.
        
        Args:
            quote: The quote to generate an image for
        
        Returns:
            PIL Image object (not base64 string)
        
        Raises:
            Exception: If image generation fails
        """
        if not self.client:
            raise Exception("GEMINI_API_KEY not found. Cannot generate image.")

        # Step 1: Generate the Image Prompt
        print(f"Generating image prompt for quote: {quote[:50]}...")
        text_prompt = IMAGE_SYSTEM_PROMPT.replace("{{quote}}", quote)
        
        text_response = self.client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[text_prompt],
        )
        
        generated_prompt = text_response.text
        print(f"Generated Image Prompt: {generated_prompt[:100]}...")

        # Extract the "Image Prompt:" part
        final_image_prompt = generated_prompt
        if "Image Prompt:" in generated_prompt:
            final_image_prompt = generated_prompt.split("Image Prompt:")[1].split("Progression Text:")[0].strip()
        
        # Step 2: Generate the Image using gemini-2.5-flash-image
        print(f"Generating image with prompt: {final_image_prompt[:50]}...")
        print(f"Using model: gemini-2.5-flash-image")
        
        image_response = None
        for attempt in range(3):
            try:
                image_response = self.client.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=[final_image_prompt],
                )
                print("Image generation API call successful!")
                break
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
                import traceback
                traceback.print_exc()
                if attempt == 2:
                    raise e
                import time
                time.sleep(2)  # Simple backoff

        # Extract image from response
        image = None
        
        for part in image_response.parts:
            if part.text is not None:
                print(f"Warning: Received text instead of image: {part.text[:100]}...")
            elif part.inline_data is not None:
                # Use as_image() method to get PIL Image directly
                try:
                    pil_image = part.as_image()
                    # Convert to RGB mode if needed and make a mutable copy
                    if pil_image.mode != 'RGB':
                        pil_image = pil_image.convert('RGB')
                    # Create a mutable copy to avoid _ensure_mutable errors
                    image = pil_image.copy()
                    print("Successfully extracted image from response!")
                    break
                except Exception as e:
                    print(f"Error using as_image(): {e}")
                    import traceback
                    traceback.print_exc()
                    # Fallback to manual extraction
                    try:
                        img_bytes = part.inline_data.data
                        pil_image = Image.open(io.BytesIO(img_bytes))
                        # Convert to RGB and make mutable copy
                        if pil_image.mode != 'RGB':
                            pil_image = pil_image.convert('RGB')
                        image = pil_image.copy()
                        print("Successfully extracted image using fallback method!")
                        break
                    except Exception as e2:
                        print(f"Fallback extraction also failed: {e2}")
                        continue
        
        if image is None:
            error_msg = "No image data found in response."
            print(f"ERROR: {error_msg}")
            print(f"Response parts: {len(image_response.parts)}")
            for i, part in enumerate(image_response.parts):
                print(f"  Part {i}: text={part.text is not None}, inline_data={part.inline_data is not None}")
            raise Exception(error_msg)
        
        return image
