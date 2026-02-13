import os
from abc import ABC, abstractmethod
from typing import Dict, Any

import src.config.settings  # Ensure environment variables are loaded

from google import genai
from google.genai import types


class BaseModel(ABC):
    """
    Base Gemini-backed LLM class.
    Handles:
    - API initialization
    - model execution
    - generation config
    """

    def __init__(self, model_name=None):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY not found in environment variables")

        self._client = genai.Client(api_key=api_key)
        if model_name is None:
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self._model_name = model_name

    # ---------- Core execution ----------

    async def _generate(self, prompt: str) -> str:
        response = ''
        for chunk in self._client.models.generate_content_stream(
            model=self._model_name,
            contents=self._wrap_prompt(prompt),
            config=self._generation_config(),
        ):
            response += chunk.text
        return response

    # ---------- Hooks for child classes ----------

    def _wrap_prompt(self, prompt: str):
        """
        Allows system/role instructions or multi-part prompting.
        Override if needed.
        """
        return prompt

    def _generation_config(self) -> types.GenerateContentConfig:
        """
        Override for tuning (temperature, top_k, etc.)
        """
        return types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=2048,
        )

    # ---------- Task contract ----------

    @abstractmethod
    async def run(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute the task and return structured output.
        """
        raise NotImplementedError
