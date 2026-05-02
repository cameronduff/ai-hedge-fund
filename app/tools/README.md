# 🛠 Tools Directory

This directory contains the functional tools that agents use to interact with the outside world or perform complex calculations.

## 📂 Tool Categories

- **`yfinance_tools.py`**: High-level functions for retrieving specific datasets from Yahoo Finance, such as balance sheets, income statements, and technical indicators.
- **`trading212_tools.py`**: Wrappers around the `Trading212Client` that expose specific actions like fetching account summaries or placing orders as tools compatible with the ADK `LlmAgent`.
- **`calculation_tools.py`**: Pure Python functions for financial mathematics, such as calculating position sizes, portfolio concentration, and volatility.

## 🛠 Tool Design

Tools are designed to be "stateless" and are often passed directly to `LlmAgent` instances. Each tool should have a clear docstring, as this is used by the LLM to understand when and how to invoke the tool.
