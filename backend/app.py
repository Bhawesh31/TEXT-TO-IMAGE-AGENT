from fastapi import FastAPI, HTTPException
from models import GenerateRequest, EditRequest, PromptResponse
from llm import enhance_prompt
from image import generate_image
from vector_db import store_prompt, get_last_prompt
from exceptions import PromptEnhancementError, ImageGenerationError, VectorDBError
from utils import get_logger

app = FastAPI(title="Text-to-Image Agent", version="1.0.0")
logger = get_logger(__name__)


@app.get("/")
def home():
    return {"message": "Text-to-Image Agent API running (Gemini Powered)", "status": "ok"}


@app.post("/generate", response_model=PromptResponse)
def generate(request: GenerateRequest):
    """Generate an image from a user concept using Gemini API"""
    try:
        logger.info(f"Generating image for: {request.user_input}")
        
        enhanced = enhance_prompt(request.user_input)
        image_data = generate_image(enhanced)
        store_prompt(enhanced)
        
        return PromptResponse(prompt=enhanced, image_data=image_data)
    
    except PromptEnhancementError as e:
        logger.error(f"Prompt enhancement error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except ImageGenerationError as e:
        logger.error(f"Image generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in generate: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/edit", response_model=PromptResponse)
def edit(request: EditRequest):
    """Edit the last generated image with modifications using Gemini API"""
    try:
        logger.info(f"Editing with: {request.edit_text}")
        
        last = get_last_prompt()
        if not last:
            raise ValueError("No previous prompt to edit")
        
        new_prompt = f"{last}, {request.edit_text}"
        image_data = generate_image(new_prompt)
        store_prompt(new_prompt)
        
        return PromptResponse(prompt=new_prompt, image_data=image_data)
    
    except VectorDBError as e:
        logger.error(f"Vector DB error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except ImageGenerationError as e:
        logger.error(f"Image generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in edit: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")