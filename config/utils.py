import os
import requests
from PIL import ImageFont, ImageDraw

def download_font(font_url, save_path):
    if not os.path.exists(save_path):
        print(f"Downloading font from {font_url}...")
        response = requests.get(font_url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Font saved to {save_path}")
    else:
        print(f"Font already exists at {save_path}")

def get_ubuntu_font(size=40):
    import os
    font_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts")
    font_path = os.path.join(font_dir, "Ubuntu-Bold.ttf")
    # URL for Ubuntu Bold from Google Fonts (raw github link or similar reliable source)
    # Using a reliable raw link for Ubuntu font
    font_url = "https://github.com/google/fonts/raw/main/ufl/ubuntu/Ubuntu-Bold.ttf"
    
    try:
        download_font(font_url, font_path)
        return ImageFont.truetype(font_path, size)
    except Exception as e:
        print(f"Error loading Ubuntu font: {e}. Falling back to default.")
        return ImageFont.load_default()

def draw_text_with_shadow(draw, position, text, font, fill="white", shadow_color="black", shadow_offset=(2, 2)):
    x, y = position
    # Draw shadow
    draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow_color, anchor="mm")
    # Draw text
    draw.text((x, y), text, font=font, fill=fill, anchor="mm")

def wrap_text(text, font, max_width, draw):
    lines = []
    words = text.split()
    current_line = []
    
    for word in words:
        current_line.append(word)
        line_width = draw.textlength(" ".join(current_line), font=font)
        if line_width > max_width:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(" ".join(current_line))
        
    return lines
