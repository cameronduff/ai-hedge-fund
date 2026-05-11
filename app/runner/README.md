# 🏃 Runner Directory

This directory contains the execution logic for running the agentic workflows.

## 📂 Key Files

- **`runner.py`**: Contains the `run_stage` utility function, which encapsulates the logic for executing a specific stage of the pipeline (creating events, handling responses, and returning the final state).

## 🛠 Orchestration

The `runner` directory provides the glue between `main.py` and the ADK's `Runner`. It handles the iterative process of sending messages to agents, logging their "thoughts" and actions, and extracting the final structured output from the session state.
