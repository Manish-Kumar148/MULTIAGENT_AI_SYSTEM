import streamlit as st
from dotenv import load_dotenv
import time

from core.llm import LLMService
from orchestrator.engine import WorkflowOrchestrator
from core.models import Task

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Multi-Agent AI System", page_icon="🤖", layout="wide")

st.title("🤖 Multi-Agent AI System")
st.markdown("A modular system with Planner, Executor, and Reviewer agents.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key (optional if in .env)", type="password")
    
    if api_key:
        import os
        os.environ["GEMINI_API_KEY"] = api_key

main_objective = st.text_area("Enter your main task objective:", height=100, placeholder="e.g., Write a comprehensive guide on building a REST API with FastAPI and Python.")

if st.button("Start Workflow", type="primary"):
    if not main_objective:
        st.error("Please enter a task objective.")
    else:
        # Initialize services
        llm_service = LLMService()
        orchestrator = WorkflowOrchestrator(llm_service)

        # Placeholders for dynamic UI updates
        status_placeholder = st.empty()
        progress_bar = st.progress(0)
        task_container = st.container()

        def update_ui(task: Task):
            # Update status
            status_placeholder.info(f"**Overall Status**: {task.status}")
            
            # Calculate progress
            if not task.subtasks:
                progress = 0.1 if task.status == "PLANNING" else 0.0
            else:
                completed = sum(1 for s in task.subtasks if s.status == "COMPLETED")
                progress = min((completed / len(task.subtasks)) * 0.9 + 0.1, 1.0)
            
            progress_bar.progress(progress)
            
            # Update Subtasks UI
            with task_container:
                # Clear previous render using a trick (we can't easily clear a container in Streamlit without rerunning, 
                # but we can use st.empty() for each subtask if we pre-allocate them)
                pass # Handled below

        # Initialize UI placeholders for subtasks once planning is done
        subtask_placeholders = []
        
        def render_callback(task: Task):
            update_ui(task)
            
            # Dynamically create placeholders if they don't exist yet (after planning)
            if task.subtasks and len(subtask_placeholders) != len(task.subtasks):
                subtask_placeholders.clear()
                with task_container:
                    st.markdown("### Subtasks Workflow")
                    for _ in task.subtasks:
                        subtask_placeholders.append(st.empty())
            
            # Render each subtask
            for i, subtask in enumerate(task.subtasks):
                if i < len(subtask_placeholders):
                    with subtask_placeholders[i].container():
                        with st.expander(f"Subtask {subtask.id}: {subtask.description[:50]}... [{subtask.status}]", expanded=(subtask.status not in ["COMPLETED", "PENDING"])):
                            st.write(f"**Description:** {subtask.description}")
                            st.write(f"**Expected Output:** {subtask.expected_output}")
                            
                            if subtask.result:
                                st.markdown("#### Result")
                                st.info(subtask.result)
                                
                            if subtask.feedback:
                                st.markdown("#### Reviewer Feedback")
                                if "REJECTED" in subtask.status:
                                    st.error(subtask.feedback)
                                else:
                                    st.success(subtask.feedback)
            time.sleep(0.5) # small delay to visualize changes

        # Run Workflow
        with st.spinner("Workflow is running..."):
            final_task = orchestrator.run_workflow(main_objective, callback=render_callback)
            
        if final_task.status == "COMPLETED":
            st.success("Workflow completed successfully!")
            progress_bar.progress(1.0)
        else:
            st.error(f"Workflow ended with status: {final_task.status}")
