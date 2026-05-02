# 🏃 Runner Directory

This directory contains the execution logic for running the agentic workflows.

## 📂 Key Files

- **`runner.py`**: Provides utilities for setting up and executing ADK `Runner` instances.
- **`retry_agent_wrapper.py`**: (If applicable) Logic for wrapping agents with retry mechanisms for increased robustness.

## 🛠 Orchestration

While `main.py` defines the high-level pipeline, the `runner` directory contains the reusable logic that handles session management, plugin integration (like `ReflectAndRetryToolPlugin`), and the actual invocation of agents.
