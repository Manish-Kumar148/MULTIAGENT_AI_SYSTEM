from abc import ABC, abstractmethod
from core.llm import LLMService

class BaseAgent(ABC):
    def __init__(self, name: str, llm_service: LLMService):
        self.name = name
        self.llm = llm_service

    @abstractmethod
    def run(self, *args, **kwargs):
        """Execute the agent's main logic."""
        pass
