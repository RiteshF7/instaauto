import sys
import os
# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from services.quote_service import QuoteService
from services.image_service import ImageService
from services.text_overlay_service import TextOverlayService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Services
quote_service = QuoteService()
image_service = ImageService()
text_overlay_service = TextOverlayService()

class GenerateRequest(BaseModel):
    prompt: str
    description: str = ""

class GenerateResponse(BaseModel):
    quote: str
    image_url: str
    caption: str

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    logger.info(f"Received generation request: {request.prompt}")
    try:
        # 1. Generate Quote
        quote = quote_service.generate_quote(request.prompt, request.description)
        logger.info(f"Generated quote: {quote}")

        # 2. Generate Caption (Parallelizable, but sequential for now)
        caption = quote_service.generate_caption(quote)
        logger.info("Generated caption")

        # 3. Generate Image
        try:
            generated_image = image_service.generate_image(quote)
            logger.info("Image generated successfully")
            
            # 4. Overlay text on image
            final_image = text_overlay_service.overlay_text(generated_image, quote)
            logger.info("Text overlaid on image")
            
            # 5. Convert to base64 data URL
            image_url = text_overlay_service.image_to_base64(final_image)
            logger.info("Image converted to base64")
        except Exception as e:
            logger.error(f"Error generating/processing image: {e}")
            image_url = "https://placehold.co/600x400?text=Error+Generating+Image"

        return GenerateResponse(quote=quote, image_url=image_url, caption=caption)

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("🚀 Server starting...")
    print("="*50)
    print("📱 Access the app at:")
    print("   http://localhost:8000")
    print("   http://127.0.0.1:8000")
    print("="*50 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
