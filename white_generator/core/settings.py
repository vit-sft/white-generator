import random
import string

# Immutable global settings
ALLOWED_CHARACTERS = string.ascii_letters + string.digits

LLM_TEXT_MODEL = "gemini-2.5-flash-lite"
LLM_IMAGE_MODEL = "gemini-2.5-flash-image"
BUCKET_NAME = "mtoffer-club"
AWS_REGION = "eu-north-1"
BASIC_FOLDER = "public/cached-whites/"


def generate_random_id(length: int = 8) -> str:
    return ''.join(random.choices(ALLOWED_CHARACTERS, k=length))
