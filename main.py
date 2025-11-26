from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from quote_service import QuoteService
from image_service import ImageService
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

class GenerateRequest(BaseModel):
    prompt: str
    description: str = ""

class GenerateResponse(BaseModel):
    quote: str
    image_url: str

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

        # 2. Generate Image
        image_url = image_service.generate_image(quote)
        logger.info(f"Generated image URL: {image_url}")

        return GenerateResponse(quote=quote, image_url=image_url)

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
