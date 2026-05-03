from agents.base import BaseAgent
from core.models import Subtask

class ExecutorAgent(BaseAgent):
    def run(self, subtask: Subtask, main_objective: str) -> str:
        prompt = f"""
You are an expert executor agent. Your job is to complete the following subtask.

Main Objective of the Project: {main_objective}

Subtask Description: {subtask.description}
Expected Output Format/Requirements: {subtask.expected_output}

Previous Feedback (if any): {subtask.feedback if subtask.feedback else "None"}

Please execute this task to the best of your ability and provide the final result.
"""
        
        print(f"[{self.name}] Executing Subtask {subtask.id}: {subtask.description}")
        result = self.llm.generate_text(prompt)
        print(f"[{self.name}] Finished Execution for Subtask {subtask.id}")
        return result
