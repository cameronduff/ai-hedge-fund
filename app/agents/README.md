🧠 Agents Directory: The Mixture of Experts (MoE) Engine

Welcome to the cognitive core of the AI Hedge Fund. This directory contains the multi-agent system responsible for gathering market data, generating investment alpha, debating strategies, and managing portfolio risk.

Instead of relying on a single, monolithic LLM prompt—which is prone to hallucinations and emotional biases—this architecture uses a **Mixture of Experts (MoE)** pattern. Agents are strictly compartmentalized into distinct roles, forming a pipeline where data flows up, opinions are debated, and execution is strictly bottlenecked.

---

## 📂 Directory Structure & Agent Roles

The agents are divided into three distinct tiers based on their responsibilities:

### 1. `/quants` (Stage 1: Data Collection & Feature Extraction)

The Quants are the data analysts. They do not make trading decisions and do not have opinions. Their sole purpose is to use external tools (like `yfinance`) to build a standardized, factual "Master Dossier" on a given ticker.

- **`technicals_agent.py`**: Analyzes price action, RSI, MACD, and moving averages.
- **`fundamentals_agent.py`**: Reviews balance sheets, income statements, and debt levels.
- **`valuations_agent.py`**: Calculates intrinsic value, P/E, and PEG ratios.
- **`growth_agent.py`**: Analyzes forward-looking estimates, TAM, and revenue expansion.

### 2. `/investors` (Stage 2: Alpha Generation & Debate)

The Investors represent the "Board of Directors." These agents are injected with specific system prompts embodying the philosophies of legendary investors. The **Chief Investment Officer (CIO)** reads the Master Dossier and triggers these experts to provide their individual analysis.

- **Value Focus**: `warren_buffett_agent`, `ben_graham_agent`, `aswath_damodaran_agent`, etc.
- **Growth Focus**: `cathie_wood_agent`, `phil_fisher_agent`, etc.
- **Risk/Contrarian Focus**: `michael_burry_agent`, `nassim_taleb_agent`, etc.

### 3. `/management` (Stage 3: Portfolio & Risk)

The Management tier governs the workflow, resolves conflicting opinions from the Investors, and applies strict constraints before any trades are proposed.

- **`portfolio_manager_agent.py`**: Aggregates the signals from the CIO and proposes a specific trade block (e.g., "Buy 5 shares of MSFT").
- **`risk_manager_agent.py`**: The ultimate gatekeeper. It is called as a tool by the Portfolio Manager to check proposals against current account balances, portfolio weighting, and volatility metrics. It has absolute power to **Approve**, **Modify**, or **Reject** the trade.

---

## 🔄 The Agent Lifecycle (Run Loop)

When `main.py` initiates the fund, the flow of data is strictly linear:

1. **Quant Analysis:** `quants_orchestrator_agent` builds a Master Dossier for all target tickers.
2. **Boardroom Debate:** The `investors_orchestrator_agent` (via the CIO) gathers independent evaluations from the individual `/investors`.
3. **Portfolio Management:** The `portfolio_manager_agent` reviews CIO recommendations and consults the `risk_manager_agent` to validate every trade.
4. **Deterministic Execution:** Approved trade instructions are returned to `main.py` for execution.

---

## 🛑 Important Architectural Guardrails

- **No Direct Execution:** **NO AGENT IN THIS DIRECTORY HAS WRITE-ACCESS TO THE BROKER.** Agents are strictly limited to read-only tools and logic. The final, approved trade instructions are passed back to `main.py`, which uses the `Trading212Client` to hit the API deterministically.
- **Tool Isolation:** Only the `/quants` have access to data-fetching tools (Yahoo Finance). Only the `/management` tier has access to read-only broker tools (checking account balance, active positions). The `/investors` are explicitly denied tool access to ensure they focus purely on qualitative analysis of the provided dossier.

---

## 🛠 Adding a New Agent

To add a new persona to the system (e.g., a new investor):

1. Create a new directory in `investors/` (e.g., `investors/ray_dalio_agent/`).
2. Define the agent's logic in `agent.py` and its system prompt in `prompt.py`.
3. Register the agent in the `chief_investment_officer/agent.py` tool list and prompt.
