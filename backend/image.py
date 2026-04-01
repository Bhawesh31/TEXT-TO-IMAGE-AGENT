import google.generativeai as genai
from utils import get_logger
from exceptions import ImageGenerationError
from config import settings

logger = get_logger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)


def generate_image(prompt: str) -> str:
    """
    Generate an image from a prompt using Gemini API (Imagen model).
    
    Args:
        prompt: Detailed image prompt
    
    Returns:
        Image data (as base64 encoded content or URL reference)
    
    Raises:
        ImageGenerationError: If image generation fails
    """
    try:
        if not prompt or not isinstance(prompt, str):
            raise ImageGenerationError("Invalid prompt")
        
        if not settings.GEMINI_API_KEY:
            raise ImageGenerationError("GEMINI_API_KEY not configured")
        
        model = genai.GenerativeModel(settings.GEMINI_MODEL_IMAGE)
        
        response = model.generate_content(prompt)
        
        if response.parts:
            image_data = response.parts[0]
            logger.info(f"Generated image for prompt: {prompt[:30]}...")
            return image_data
        else:
            raise ImageGenerationError("No image data returned from API")
    
    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        raise ImageGenerationError(f"Failed to generate image: {str(e)}")