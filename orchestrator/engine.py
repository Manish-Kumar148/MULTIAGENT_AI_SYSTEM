from typing import Callable, Optional
from core.models import Task, Subtask
from core.llm import LLMService
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.reviewer import ReviewerAgent

class WorkflowOrchestrator:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        self.planner = PlannerAgent("Planner", self.llm)
        self.executor = ExecutorAgent("Executor", self.llm)
        self.reviewer = ReviewerAgent("Reviewer", self.llm)
        self.max_retries = 3

    def run_workflow(self, main_objective: str, callback: Optional[Callable[[Task], None]] = None) -> Task:
        """Runs the entire multi-agent workflow."""
        task = Task(main_objective=main_objective)
        
        # 1. Planning Phase
        task.status = "PLANNING"
        if callback: callback(task)
        
        planner_output = self.planner.run(task)
        task.subtasks = planner_output.subtasks
        
        # 2. Execution & Review Phase
        task.status = "IN_PROGRESS"
        if callback: callback(task)
        
        for subtask in task.subtasks:
            subtask.status = "IN_PROGRESS"
            if callback: callback(task)
            
            retries = 0
            approved = False
            
            while not approved and retries < self.max_retries:
                # Execution
                result = self.executor.run(subtask, task.main_objective)
                subtask.result = result
                if callback: callback(task)
                
                # Review
                review = self.reviewer.run(subtask, task.main_objective)
                subtask.feedback = review.feedback
                
                if review.approved:
                    approved = True
                    subtask.status = "COMPLETED"
                else:
                    retries += 1
                    subtask.status = f"REJECTED (Retry {retries}/{self.max_retries})"
                
                if callback: callback(task)
                
            if not approved:
                # If we exceed max retries, we mark the subtask and whole task as failed
                subtask.status = "FAILED"
                task.status = "FAILED"
                if callback: callback(task)
                return task
                
        task.status = "COMPLETED"
        if callback: callback(task)
        return task
