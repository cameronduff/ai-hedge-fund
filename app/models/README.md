# 📊 Models Directory

This directory contains the data structures and validation logic used throughout the application, primarily defined using Pydantic models.

## 📂 Model Categories

- **`quants_models.py`**: Defines the schemas for raw data extracted by Quant agents, including `Ticker`, `Dossier`, and individual quant outputs (Fundamentals, Technicals, etc.).
- **`investors_models.py`**: Contains models for investment decisions, ratings, and the structured output of the Chief Investment Officer.
- **`management_models.py`**: Defines `TradeInstruction` and `PortfolioManagerOutput`, which govern how trade proposals are structured and risk-approved.
- **`trading212_models.py`**: Low-level models representing payloads for the Trading 212 API (e.g., `LimitOrderPayload`).

## 🛠 Importance of Schemas

These models are critical for the "Mixture of Experts" architecture. They ensure that every agent in the pipeline receives and produces strictly validated JSON, preventing the "unstructured text" issues common in simple LLM chains.
