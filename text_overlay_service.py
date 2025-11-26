"""
Text Overlay Service
Handles overlaying text on images with proper formatting and styling.
"""
import io
import base64
from PIL import Image, ImageDraw
from utils import get_ubuntu_font, draw_text_with_shadow, wrap_text


class TextOverlayService:
    """Service for overlaying text on images"""
    
    def overlay_text(self, image: Image.Image, quote: str, position: str = "bottom_center") -> Image.Image:
        """
        Overlays text on an image.
        
        Args:
            image: PIL Image object to overlay text on
            quote: Text to overlay
            position: Position of text ("bottom_center", "center", "top_center")
        
        Returns:
            PIL Image with text overlaid
        """
        # Ensure image is mutable and in RGB mode
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.copy()
        
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        # Font setup
        font_size = int(width * 0.032)  # Slightly smaller dynamic font size based on width
        font = get_ubuntu_font(font_size)
        
        # Wrap text
        margin = int(width * 0.1)
        max_text_width = width - (2 * margin)
        lines = wrap_text(quote, font, max_text_width, draw)
        
        # Calculate total text height
        line_height = font.getbbox("Ay")[3] + 10  # approximate height + padding
        total_text_height = len(lines) * line_height
        
        # Position calculation
        if position == "bottom_center":
            start_y = height - int(height * 0.25) - (total_text_height // 2)
        elif position == "center":
            start_y = (height // 2) - (total_text_height // 2)
        elif position == "top_center":
            start_y = int(height * 0.1)
        else:
            start_y = height - int(height * 0.25) - (total_text_height // 2)
        
        # Draw text lines
        current_y = start_y
        for line in lines:
            # Draw centered text with shadow
            draw_text_with_shadow(draw, (width // 2, current_y), line, font)
            current_y += line_height
        
        return image
    
    def image_to_base64(self, image: Image.Image, mime_type: str = "image/png") -> str:
        """
        Converts a PIL Image to a base64 data URL.
        
        Args:
            image: PIL Image object
            mime_type: MIME type of the image (default: "image/png")
        
        Returns:
            Base64 data URL string
        """
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        b64_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return f"data:{mime_type};base64,{b64_str}"

