from agents.base import BaseAgent
from core.models import Subtask, ReviewResult

class ReviewerAgent(BaseAgent):
    def run(self, subtask: Subtask, main_objective: str) -> ReviewResult:
        prompt = f"""
You are a strict and detail-oriented Reviewer Agent. Your job is to review the output of an Executor Agent.

Main Objective: {main_objective}

Subtask Details:
Description: {subtask.description}
Expected Output: {subtask.expected_output}

Executor's Output:
{subtask.result}

Evaluate the Executor's Output against the Subtask Details.
If the output meets the requirements, approve it. If not, reject it and provide specific feedback on what needs to be fixed.
"""
        
        print(f"[{self.name}] Reviewing Subtask {subtask.id}")
        result = self.llm.generate_structured(prompt, ReviewResult)
        
        status_msg = "APPROVED" if result.approved else "REJECTED"
        print(f"[{self.name}] Review Result for Subtask {subtask.id}: {status_msg}")
        return result
