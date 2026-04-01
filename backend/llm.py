import google.generativeai as genai
from utils import get_logger
from exceptions import PromptEnhancementError
from config import settings

logger = get_logger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)


def enhance_prompt(user_input: str) -> str:
    """
    Enhance user input into a detailed image prompt using Gemini API.
    
    Args:
        user_input: Basic user concept (e.g., "car")
    
    Returns:
        Enhanced prompt with style, lighting, and environment details
    
    Raises:
        PromptEnhancementError: If enhancement fails
    """
    try:
        if not user_input or not isinstance(user_input, str):
            raise PromptEnhancementError("Invalid user input")
        
        if not settings.GEMINI_API_KEY:
            raise PromptEnhancementError("GEMINI_API_KEY not configured")
        
        model = genai.GenerativeModel(settings.GEMINI_MODEL_TEXT)
        
        prompt = f"""You are an expert art director for image generation. 
Enhance the following concept into a detailed, vivid image prompt for an AI image generator.
Include: style, lighting, environment, camera angle, mood, and artistic details.
Keep it under 150 words.

Concept: {user_input}

Enhanced Prompt:"""
        
        response = model.generate_content(prompt)
        enhanced = response.text.strip()
        
        logger.info(f"Enhanced prompt for input: {user_input[:30]}...")
        return enhanced
    
    except Exception as e:
        logger.error(f"Prompt enhancement failed: {e}")
        raise PromptEnhancementError(f"Failed to enhance prompt: {str(e)}")