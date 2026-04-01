from pydantic import BaseModel
from typing import Union


class GenerateRequest(BaseModel):
    user_input: str


class EditRequest(BaseModel):
    edit_text: str


class PromptResponse(BaseModel):
    prompt: str
    image_data: Union[str, dict]  # Can be URL string or image data


class ImageResponse(BaseModel):
    image_data: Union[str, dict]
