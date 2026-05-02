# 🤖 AI Hedge Fund: A Mixture of Experts (MoE) Trading Platform

Welcome to the **AI Hedge Fund**, a sophisticated multi-agent system designed to automate equity research, investment debate, and trade execution. 

Instead of relying on a single monolithic AI, this platform utilizes a **Mixture of Experts (MoE)** architecture. It breaks down the complex task of "investing" into discrete, specialized roles—from quantitative analysis to philosophical investment debate—culminating in a deterministic execution layer.

---

## 🏛 Architecture Overview

The system operates in four distinct phases:

1.  **Phase 1: Quant Analysis:** Specialized agents (`fundamentals`, `technicals`, `growth`, `valuations`) gather raw data via Yahoo Finance to build a factual "Master Dossier."
2.  **Phase 2: Investor Boardroom:** A diverse group of "Persona Agents" (Buffett, Graham, Burry, Wood, etc.) reviews the dossier and provides independent ratings and rationales.
3.  **Phase 3: Portfolio Management:** The `Chief Investment Officer` and `Portfolio Manager` aggregate these opinions, break ties, and propose specific trade blocks.
4.  **Phase 4: Risk & Execution:** The `Risk Manager` validates proposals against account balances and volatility. Approved trades are then deterministically executed via the **Trading 212 API**.

---

## 📂 Project Structure

-   **`app/agents/`**: The cognitive core. Contains the Quants, Investors, and Management agents.
-   **`app/clients/`**: Low-level API clients for Trading 212 and Yahoo Finance.
-   **`app/models/`**: Pydantic schemas that ensure type-safe data flow between agents.
-   **`app/tools/`**: Functional tools (data fetching, math) used by agents.
-   **`app/core/`**: Centralized configuration and settings.
-   **`app/runner/`**: Reusable logic for executing ADK-based agent workflows.
-   **`main.py`**: The main entry point that orchestrates the entire pipeline.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip`
- Google Gemini API Key
- Trading 212 API Key (Demo account recommended)

### 2. Installation
```bash
# Clone the repository
git clone <repo-url>
cd ai-hedge-fund

# Install dependencies
uv sync
```

### 3. Configuration
Create a `.env.local` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key
TRADING_212_API_KEY=your_t212_api_key
TRADING_212_API_SECRET=your_t212_api_secret

# Optional: Override default models
REASONING_MODEL=gemini-3.1-pro-preview
FORMATTING_MODEL=gemini-5.5-flash
```

### 4. Running the Fund
```bash
python -m app.main
```

---

## 🛡️ Security & Guardrails

-   **Deterministic Execution:** Agents can suggest trades but **cannot** execute them directly. The final execution is handled by a strictly typed Python layer after risk approval.
-   **Retry Logic:** All agents are configured with HTTP retry options and exponential backoff to gracefully handle rate limits (429 errors).
-   **Memory Safety:** The system uses `InMemorySessionService` for short-lived, context-efficient research sessions.

---

## 📜 License
[MIT License](LICENSE)
