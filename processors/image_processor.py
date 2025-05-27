"""Image processing and analysis."""

import base64
import io
from typing import Dict, Any, BinaryIO
from config.settings import Config

try:
    from PIL import Image
    IMAGE_SUPPORT = True
except ImportError:
    IMAGE_SUPPORT = False

class ImageProcessor:
    """Handle image processing and analysis."""
    
    @staticmethod
    def is_supported() -> bool:
        """Check if image processing is supported."""
        return IMAGE_SUPPORT
    
    @staticmethod
    def process_image(uploaded_file: BinaryIO) -> Dict[str, Any]:
        """Process uploaded image and prepare for AI analysis."""
        if not IMAGE_SUPPORT:
            return {
                "success": False,
                "error": "Image processing not supported. Please install Pillow."
            }
        
        try:
            image = Image.open(uploaded_file)
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            width, height = image.size
            file_size = getattr(uploaded_file, 'size', 0)
            
            # Resize if too large (Gemini has size limits)
            max_size = Config.MAX_IMAGE_SIZE
            if width > max_size or height > max_size:
                ratio = min(max_size/width, max_size/height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to base64
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG", quality=85)
            img_bytes = buffered.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode()
            
            return {
                "success": True,
                "base64_data": img_base64,
                "original_size": (width, height),
                "processed_size": image.size,
                "file_size": file_size,
                "format": image.format or "JPEG"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }