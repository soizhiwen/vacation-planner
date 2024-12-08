import os
import logging

gpt_key = os.environ.get("OPENAI_API_KEY")
gpt_model = os.environ.get("GPT_MODEL")

logger = logging.getLogger("uvicorn.error")
