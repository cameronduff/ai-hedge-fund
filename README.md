# AI Hedge Fund (Educational Prototype)

This repository is a simplified, agent‑oriented prototype exploring how multiple investing philosophies and analytical lenses can be orchestrated with LLMs. It is adapted from an upstream project but pared down: there is currently no web app, no backtester module, and no CLI flags for multi‑ticker/date range operation. The current code focuses on composing agents in a pipeline and providing a standalone Trading 212 client for experimentation.

> IMPORTANT: This project is for educational and research purposes only. It does not execute real trades automatically. Nothing here constitutes investment advice.

## Core Concepts

The system builds an agent pipeline (see `src/pipeline.py`) combining:

Research Agents (run in parallel):

- Fundamentals Agent
- Technicals Agent
- Sentiment Agent
- Valuation Agent

Investor Philosophy Agents (run in parallel):

- Aswath Damodaran
- Ben Graham
- Bill Ackman
- Cathie Wood
- Charlie Munger
- Michael Burry
- Mohnish Pabrai
- Peter Lynch
- Phil Fisher
- Rakesh Jhunjhunwala
- Stanley Druckenmiller
- Warren Buffett

Execution Layer (sequential):

- Risk Manager
- Portfolio Manager

Each agent has a prompt and schema under `src/agents/...` and is aggregated into a looping composite (`LoopAgent`) with retry wrapping to handle transient LLM/API errors.

## Current State / What Works

- Pipeline construction (`get_pipeline`) and a demonstrative run in `src/pipeline.py` (currently using a sample GCS video input — a placeholder to prove invocation mechanics).
- Runner utilities in `src/runner.py` to execute the pipeline asynchronously and harvest final consensus output.
- A fully featured Trading 212 client + CLI in `src/clients/Trading212.py` supporting account inspection, portfolio, orders (demo/live), pies, history, metadata, quotes (Yahoo Finance), and simple agent‑style trade helpers.

## What Is NOT Present (Yet)

- Backtesting module referenced in the original upstream README.
- Web application / UI.
- Multi‑ticker orchestration and date‑window analysis CLI.
- Integrated financial datasets ingestion (only the skeleton/agents exist; data pulls are not wired here).

## Installation

The project uses `pyproject.toml` (PEP 621). Dependencies are minimal.

```bash
git clone https://github.com/cameronduff/ai-hedge-fund.git
cd ai-hedge-fund
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -e .
```

Or, if you prefer just installing dependencies:

```bash
pip install .
```

Python 3.13+ is specified in `pyproject.toml` (adjust locally if needed).

## Configuration (Environment Variables)

Only the Trading 212 client currently consumes environment variables:

Required for CLI operations:

- `T212_API_KEY` – Trading 212 API key
- `T212_API_SECRET` – Trading 212 API secret

Optional:

- `T212_ENV` – `demo` (default) or `live`
- `T212_BASE_URL` – override base API URL (useful for mocking)

Example `.env` (create manually – there is no template yet):

```
T212_API_KEY=your_key_here
T212_API_SECRET=your_secret_here
T212_ENV=demo
```

Load it (if desired) with a tool like `python-dotenv` or by exporting directly in your shell.

## Running the Agent Pipeline

For now the main entry point (`main.py`) just prints a greeting. To execute the pipeline demo:

```bash
python src/pipeline.py
```

This will:

1. Build the composite agent pipeline.
2. Run it against a placeholder GCS video URI (replace with your own input if adapting the content modality).
3. Log events and final output via `loguru`.

If you adapt it to text inputs, modify the invocation in the `__main__` block of `src/pipeline.py` to construct a `types.Content` with textual parts instead of a video URI.

## Using the Trading 212 CLI

The client resides at `src/clients/Trading212.py` and can be executed directly once environment variables are set.

List available commands:

```bash
python src/clients/Trading212.py --help
```

Examples:

```bash
# Account & portfolio
python src/clients/Trading212.py cash
python src/clients/Trading212.py account
python src/clients/Trading212.py portfolio
python src/clients/Trading212.py position AAPL

# Market data (Yahoo Finance)
python src/clients/Trading212.py quote AAPL

# Place a market order (BUY 1 share AAPL demo env)
python src/clients/Trading212.py buy AAPL 1

# Simple decision helper
python src/clients/Trading212.py agent-decide VUSA VUSA.L --threshold 1.0
```

Note: In live environment only market orders are supported; a SELL uses negative quantity internally (handled for you by `agent.sell`).

## Roadmap / Ideas

- Add real fundamental + sentiment data ingestion layer (financial APIs, news feeds).
- Implement backtester harness for agent consensus strategies.
- Web dashboard for agent outputs, risk metrics, and trade recommendations.
- Persistent session storage (database) instead of in‑memory.
- Unit tests & CI workflow.
- `.env.example` and secrets management guidance.
- Expand agent decision logic to yield structured trade recommendations.

## Contributing

Pull requests are welcome. Please keep them focused and small (one feature or fix per PR). Suggested approach:

1. Open an issue describing desired change.
2. Branch from `main`.
3. Implement + add minimal tests if code behavior changes.
4. Submit PR referencing the issue.

## Disclaimer

Use at your own risk. No warranties, no guarantees of performance. This software does not provide investment advice and should not be used for real-money decision making without independent verification.

## License

MIT License. See `LICENSE` (add if missing).

## Attribution

Inspired by an upstream AI hedge fund concept; reworked to match the current trimmed feature set.

---

If you extend this project (e.g., backtesting or UI), remember to update this README accordingly.
