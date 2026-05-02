# 🤖 AI Hedge Fund: A Mixture of Experts (MoE) Trading Platform

Welcome to the **AI Hedge Fund**, a sophisticated multi-agent system designed to automate equity research, investment debate, and trade execution. 

This project is inspired by the excellent work of [Virat Singh](https://github.com/virattt/ai-hedge-fund). It re-imagines the original concept using the **Google Agent Developer Kit (ADK)** and the **Gemini 2.0** suite of models to create a highly scalable, type-safe, and robust investment pipeline.

---

## 🏛 The Multi-Phase Pipeline

Instead of a single prompt, the fund operates through a strictly linear, four-phase pipeline:

### Phase 1: Quantitative Analysis (The Quants)
The Quants are the data analysts. Their sole purpose is to build a standardized, factual "Master Dossier" using tools like `yfinance`.
- **Technicals:** Analyzes price action, RSI, MACD, and moving averages.
- **Fundamentals:** Dissects balance sheets, income statements, and cash flows.
- **Valuations:** Calculates intrinsic value using DCF, P/E, and PEG ratios.
- **Growth:** Evaluates revenue expansion and forward-looking catalysts.

### Phase 2: The Investor Boardroom (Alpha Generation)
The dossier is presented to a diverse board of "Persona Agents," each embodying a specific investment philosophy. They debate the findings and output a structured rating (`BUY`, `SELL`, `HOLD`) and conviction score.
- **The Value Legends:** Warren Buffett, Ben Graham, and Aswath Damodaran focus on margin of safety and intrinsic value.
- **The Growth Visionaries:** Cathie Wood and Phil Fisher look for disruptive innovation and long-term scaling.
- **The Risk Specialists:** Nassim Taleb and Michael Burry hunt for tail risks and systemic fragility.
- **The Tactical Traders:** Stanley Druckenmiller and Bill Ackman analyze macro positioning and reflexive market moves.

### Phase 3: Portfolio Management (Decision Synthesis)
The **Chief Investment Officer (CIO)** and **Portfolio Manager** aggregate the conflicting signals from the Boardroom. They resolve debates, apply macro overlays, and propose specific trade instructions (e.g., "Add 10 shares of MSFT at £420").

### Phase 4: Risk Control & Execution (The Gatekeeper)
The **Risk Manager** is the final bottleneck. It reviews the proposal against real-time account data from **Trading 212**. It validates position sizes, portfolio concentration, and volatility before providing final approval. Approved trades are then deterministically executed via the Trading 212 API.

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
