# 🤖 Multi-Agent AI System

A modular, state-of-the-art multi-agent orchestration framework built with Python, Pydantic, and Google's Gemini Flash. This system implements a sophisticated **Plan-Execute-Review** workflow where specialized agents collaborate to solve complex, high-level objectives with high reliability.

---

## 🌟 Key Features

- **Modular Agent Architecture**: Separated concerns between Planner, Executor, and Reviewer agents.
- **Structured Logic**: Uses Pydantic models to ensure strict communication protocols and zero-shot schema adherence.
- **Intelligent Feedback Loop**: Automatic rework cycle where the Reviewer can send tasks back to the Executor with specific feedback.
- **Real-time Dashboard**: Interactive Streamlit-based UI to visualize the agentic reasoning and execution steps.
- **Graceful Mock Fallback**: Runs in simulation mode if no API key is provided, perfect for demos.

---

## 🏗️ Architecture

The system follows a sequential chain managed by a **Workflow Orchestrator**:

1.  **Planner Agent**: Deconstructs the main objective into actionable subtasks.
2.  **Executor Agent**: Performs the heavy lifting for each subtask.
3.  **Reviewer Agent**: Validates outputs against original requirements. If rejected, it triggers a retry loop.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A Google Gemini API Key (Get one for free at [Google AI Studio](https://aistudio.google.com/app/apikey))

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Manish-Kumar148/MULTIAGENT_AI_SYSTEM.git
    cd MULTIAGENT_AI_SYSTEM
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory:
    ```bash
    GEMINI_API_KEY=your_api_key_here
    ```

### Running the App

Launch the interactive dashboard with Streamlit:

```bash
python -m streamlit run app.py
```

Open the URL provided (usually `http://localhost:8501`) in your browser to start using the system.

---

## 👤 Author

**Manish Kumar**
- GitHub: [@Manish-Kumar148](https://github.com/Manish-Kumar148)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
