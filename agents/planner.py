from agents.base import BaseAgent
from core.models import Task, PlannerOutput

class PlannerAgent(BaseAgent):
    def run(self, task: Task) -> PlannerOutput:
        prompt = f"""
You are an expert project planner. Break down the following main objective into a logical sequence of subtasks.
Each subtask must be specific, actionable, and contribute directly to the main objective.

Main Objective: {task.main_objective}

Provide the output as a structured list of subtasks.
"""
        
        print(f"[{self.name}] Planning task: {task.main_objective}")
        output = self.llm.generate_structured(prompt, PlannerOutput)
        
        # Ensure sequential IDs and initial status
        for i, subtask in enumerate(output.subtasks):
            subtask.id = i + 1
            subtask.status = "PENDING"
            
        print(f"[{self.name}] Generated {len(output.subtasks)} subtasks.")
        return output
