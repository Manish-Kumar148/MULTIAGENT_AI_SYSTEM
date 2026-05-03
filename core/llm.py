import os
import json
from pydantic import BaseModel
from typing import Type, TypeVar, Optional, Any

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

T = TypeVar('T', bound=BaseModel)

class LLMService:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.model_name = model_name
        
        if HAS_GENAI and self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def generate_structured(self, prompt: str, response_schema: Type[T]) -> T:
        """Generates a structured response based on the provided Pydantic model."""
        if not self.client:
            return self._mock_structured_response(prompt, response_schema)

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_schema,
                    temperature=0.2,
                ),
            )
            # The response.text should be a JSON string that parses to our schema
            data = json.loads(response.text)
            return response_schema(**data)
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return self._mock_structured_response(prompt, response_schema)

    def generate_text(self, prompt: str) -> str:
        """Generates plain text response."""
        if not self.client:
            return self._mock_text_response(prompt)

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                )
            )
            return response.text
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return self._mock_text_response(prompt)

    def _mock_structured_response(self, prompt: str, response_schema: Type[T]) -> T:
        """Provides a dummy structured response when API is unavailable."""
        print("[MOCK] Generating dummy structured response.")
        
        if response_schema.__name__ == "PlannerOutput":
            from core.models import Subtask
            return response_schema(
                subtasks=[
                    Subtask(
                        id=1,
                        description="Mock subtask 1: Research the topic",
                        expected_output="A summary of research findings"
                    ),
                    Subtask(
                        id=2,
                        description="Mock subtask 2: Draft the content",
                        expected_output="A draft document"
                    )
                ]
            )
        elif response_schema.__name__ == "ReviewResult":
            return response_schema(
                approved=True,
                feedback="Mock feedback: This looks good and meets all requirements."
            )
            
        # Generic mock (may fail validation if model has strict fields)
        return response_schema.model_construct()

    def _mock_text_response(self, prompt: str) -> str:
        """Provides a dummy text response when API is unavailable."""
        print("[MOCK] Generating dummy text response.")
        return "This is a simulated execution result. The task was completed successfully according to the given instructions."
