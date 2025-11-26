# InstaAuto - AI-Powered Quote & Image Generator

A FastAPI-based web application that generates space-themed quotes with AI-generated images and Instagram captions.

## Features

- 🚀 **AI Quote Generation**: Generate engaging space facts using Google Gemini
- 🎨 **AI Image Generation**: Create beautiful cosmic images with Gemini image models
- ✍️ **Text Overlay**: Automatically overlay quotes on images with professional styling
- 📱 **Instagram Captions**: Generate ready-to-use social media captions with hashtags
- 🌐 **Web Interface**: Clean, modern web UI for easy interaction

## Project Structure

```
instaauto/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create from .env.example)
├── services/               # Core business logic services
│   ├── quote_service.py    # Quote and caption generation
│   ├── image_service.py    # AI image generation
│   └── text_overlay_service.py  # Text overlay on images
├── config/                 # Configuration and utilities
│   ├── prompts.py          # AI prompts and templates
│   └── utils.py            # Utility functions (fonts, text wrapping)
├── scripts/                # Helper scripts
│   ├── start_server.py     # Server startup script with auto-browser
│   └── start.bat           # Windows batch file for easy startup
├── tests/                  # Test files
│   ├── test_api.py         # API connection tests
│   └── test_image_api.py   # Image generation tests
├── templates/              # HTML templates
│   └── index.html          # Main web interface
├── static/                 # Static assets
│   ├── style.css           # Stylesheet
│   └── script.js           # Frontend JavaScript
└── assets/                 # Generated assets
    └── fonts/              # Downloaded fonts
```

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Run the Application**
   ```bash
   # Option 1: Direct Python
   python main.py
   
   # Option 2: Using startup script (auto-opens browser)
   python scripts/start_server.py
   
   # Option 3: Windows batch file
   scripts\start.bat
   ```

4. **Access the Application**
   Open your browser and navigate to:
   - http://localhost:8000
   - http://127.0.0.1:8000

## Usage

1. Enter a space entity (e.g., "Moon", "Jupiter", "Black Holes") or click "Surprise Me" for a random selection
2. Optionally add context/description
3. Click "Generate" to create:
   - A space fact/quote
   - An AI-generated cosmic image with the quote overlaid
   - An Instagram-ready caption with hashtags
4. Download the image or copy the quote/caption

## Technologies

- **Backend**: FastAPI, Python
- **AI**: Google Gemini API (gemini-2.5-flash, gemini-2.5-flash-image)
- **Image Processing**: Pillow (PIL)
- **Frontend**: HTML, CSS, JavaScript

## Requirements

- Python 3.8+
- Google Gemini API Key
- See `requirements.txt` for Python packages

## License

MIT License

