# AI Hedge Fund

An intelligent investment analysis system that combines multiple investment philosophies and analytical approaches using AI agents to generate comprehensive trading recommendations. This system simulates how a sophisticated hedge fund might analyze securities using diverse methodologies from legendary investors and modern quantitative techniques.

## Attribution

This project is based on the original work from [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund/tree/main/src). The core architecture and agent-based approach were inspired by that implementation, with additional enhancements and modifications.

> **IMPORTANT**: This project is for educational and research purposes only. It does not execute real trades automatically. Nothing here constitutes investment advice.

## System Architecture

The AI Hedge Fund operates in three distinct phases:

### 1. Research Phase (Parallel Analysis)

Four specialized research agents analyze different aspects of securities:

- **Fundamentals Agent**: Analyzes financial statements, profitability metrics, growth rates, financial health, and valuation ratios to assess company quality
- **Technical Agent**: Performs quantitative analysis using trend indicators, momentum signals, mean reversion patterns, volatility metrics, and statistical analysis
- **Sentiment Agent**: Processes news articles and market sentiment to gauge public perception and potential catalysts
- **Valuation Agent**: Conducts intrinsic value calculations using DCF models, comparable company analysis, and various valuation methodologies

### 2. Investment Philosophy Phase (Parallel Consensus)

Twelve legendary investor agents apply their unique investment philosophies:

- **Warren Buffett**: Value investing focused on economic moats, exceptional management, and long-term compounding
- **Charlie Munger**: Mental models approach emphasizing business quality and rational decision-making
- **Ben Graham**: Deep value investing with margin of safety and quantitative screening
- **Peter Lynch**: Growth at reasonable price (GARP) with focus on understandable businesses
- **Phil Fisher**: Growth investing emphasizing innovative companies with strong management
- **Bill Ackman**: Activist investing targeting undervalued companies with catalyst potential
- **Michael Burry**: Contrarian value investing with deep fundamental analysis
- **Cathie Wood**: Disruptive innovation investing focused on transformative technologies
- **Stanley Druckenmiller**: Macro-driven investing with flexible position sizing
- **Aswath Damodaran**: Academic valuation approach with rigorous financial modeling
- **Mohnish Pabrai**: Concentrated value investing inspired by Buffett with risk management
- **Rakesh Jhunjhunwala**: Growth investing with long-term perspective and market timing

### 3. Execution Phase (Sequential Risk Management)

Two specialized agents make final decisions:

- **Risk Manager**: Analyzes volatility patterns, correlation risks, and determines appropriate position sizing based on portfolio risk metrics
- **Portfolio Manager**: Synthesizes all agent recommendations to make final trading decisions with proper position sizing and risk controls

## Features

### ✅ Current Capabilities

- **Complete Agent Pipeline**: Fully functional multi-agent system with research, philosophy, and execution phases
- **Trading 212 Integration**: Complete API client with demo/live trading capabilities
- **Comprehensive Analysis Tools**: Fundamental, technical, sentiment, and valuation analysis functions
- **Risk Management**: Volatility-based position sizing and correlation analysis
- **Async Pipeline Execution**: Parallel processing of research and investor agents for efficiency
- **Retry Logic**: Robust error handling for LLM and API failures

### 🚧 In Development

- **Real-time Data Integration**: Enhanced financial data feeds and news ingestion
- **Backtesting Framework**: Historical performance analysis of agent strategies
- **Web Dashboard**: Interactive UI for monitoring agent decisions and portfolio performance
- **Multi-ticker Analysis**: Batch processing for portfolio-wide analysis

## Installation

### Prerequisites

Install [UV](https://docs.astral.sh/uv/) - the fast Python package manager:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using Homebrew
brew install uv

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup

```bash
git clone https://github.com/cameronduff/ai-hedge-fund.git
cd ai-hedge-fund

# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

Python 3.13+ is required (adjust `pyproject.toml` if needed).

> **Note**: `uv sync` automatically creates a virtual environment (`.venv`) and installs all dependencies from `pyproject.toml` in one command.

## Configuration

### Required API Keys

Create a `.env` file in the project root with the following keys (see `.env.example` for template):

```bash
# Google Gemini API for LLM processing
GEMINI_API_KEY=your_gemini_api_key

# Trading 212 API for trade execution
T212_ENV=demo  # or 'live' for real trading
T212_API_KEY=your_trading212_api_key
T212_API_SECRET=your_trading212_api_secret

# Finnhub API for financial data
FINNHUB_API_KEY=your_finnhub_api_key

# Rate limiting for LLM calls
GENAI_LLM_RPM=2  # Requests per minute
```

### API Key Setup Guide

1. **Gemini API**: Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Trading 212 API**: Register at [Trading 212](https://www.trading212.com/) and request API access
3. **Finnhub API**: Sign up at [Finnhub](https://finnhub.io/) for free financial data access

### Environment Variables

Load environment variables using:

```bash
# Using python-dotenv (included in dependencies)
# Environment variables are automatically loaded from .env file

# Or export manually in your shell
export GEMINI_API_KEY=your_key_here
```

## Usage

### Running the AI Hedge Fund Pipeline

Execute the complete analysis pipeline:

```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # if not already activated

# Run the pipeline
uv run python -m src.pipeline

# Or alternatively (if venv is activated)
python -m src.pipeline
```

This will:

1. Initialize all research agents (fundamentals, technicals, sentiment, valuation)
2. Run all 12 investor philosophy agents in parallel
3. Apply risk management and portfolio optimization
4. Generate final trading recommendations with position sizing

### Individual Agent Testing

Test specific agents:

```bash
# Run fundamentals analysis
uv run python -m src.agents.fundamentals_agent.agent

# Test Warren Buffett investment philosophy
uv run python -m src.agents.investors.warren_buffett.agent
```

## Using the Trading 212 CLI

The client resides at `src/clients/Trading212.py` and can be executed directly once environment variables are set.

List available commands:

```bash
uv run python src/clients/Trading212.py --help
```

Examples:

```bash
# Account & portfolio
uv run python src/clients/Trading212.py cash
uv run python src/clients/Trading212.py account
uv run python src/clients/Trading212.py portfolio
uv run python src/clients/Trading212.py position AAPL

# Market data (Yahoo Finance)
uv run python src/clients/Trading212.py quote AAPL

# Place a market order (BUY 1 share AAPL demo env)
uv run python src/clients/Trading212.py buy AAPL 1

# Simple decision helper
uv run python src/clients/Trading212.py agent-decide VUSA VUSA.L --threshold 1.0
```

Note: In live environment only market orders are supported; a SELL uses negative quantity internally (handled for you by `agent.sell`).

## Agent Details

### Research Agents

| Agent            | Purpose                                           | Key Metrics                                               |
| ---------------- | ------------------------------------------------- | --------------------------------------------------------- |
| **Fundamentals** | Analyzes company financial health and performance | ROE, profit margins, debt ratios, growth rates            |
| **Technical**    | Identifies price patterns and trading signals     | Moving averages, RSI, Bollinger Bands, volume analysis    |
| **Sentiment**    | Processes news and market sentiment               | News sentiment scores, social media buzz, analyst ratings |
| **Valuation**    | Determines intrinsic value and fair price         | DCF models, P/E ratios, PEG ratios, price targets         |

### Investor Philosophy Agents

Each agent embodies the investment approach of legendary investors:

| Investor                  | Philosophy                        | Key Focus                                                           |
| ------------------------- | --------------------------------- | ------------------------------------------------------------------- |
| **Warren Buffett**        | Value investing with moats        | Quality businesses, competitive advantages, long-term holding       |
| **Charlie Munger**        | Rational thinking & mental models | Business quality, avoiding mistakes, patient capital                |
| **Ben Graham**            | Deep value & margin of safety     | Quantitative screening, asset values, statistical cheapness         |
| **Peter Lynch**           | Growth at reasonable price        | Understandable businesses, earnings growth, reasonable valuations   |
| **Phil Fisher**           | Growth investing                  | Innovation, management quality, sustainable growth                  |
| **Bill Ackman**           | Activist value investing          | Undervalued companies, catalyst events, management changes          |
| **Michael Burry**         | Contrarian deep value             | Overlooked opportunities, intensive research, market inefficiencies |
| **Cathie Wood**           | Disruptive innovation             | Transformative technologies, exponential growth, future trends      |
| **Stanley Druckenmiller** | Macro-driven flexible approach    | Market timing, position sizing, risk management                     |
| **Aswath Damodaran**      | Academic valuation rigor          | Financial modeling, valuation metrics, data-driven decisions        |
| **Mohnish Pabrai**        | Concentrated value investing      | High-conviction bets, Buffett-inspired approach, risk management    |
| **Rakesh Jhunjhunwala**   | Growth with market timing         | Indian market expertise, growth companies, long-term vision         |

### Execution Agents

| Agent                 | Purpose                                     | Key Functions                                                |
| --------------------- | ------------------------------------------- | ------------------------------------------------------------ |
| **Risk Manager**      | Controls position sizing and portfolio risk | Volatility analysis, correlation assessment, position limits |
| **Portfolio Manager** | Makes final trading decisions               | Signal aggregation, position sizing, execution timing        |

## Project Structure

```
src/
├── agents/                 # All AI agents
│   ├── fundamentals_agent/ # Financial analysis
│   ├── technicals_agent/   # Technical analysis
│   ├── sentiment_agent/    # News sentiment
│   ├── valuation_agent/    # Intrinsic value
│   ├── investors/          # Legendary investor philosophies
│   ├── risk_manager/       # Risk assessment
│   └── portfolio_manager/  # Final decisions
├── clients/                # External API clients
│   ├── FinnhubClient.py   # Financial data
│   └── Trading212.py      # Brokerage integration
├── tools/                  # Analysis functions
└── utils/                  # Helper utilities
```

## Roadmap

- [ ] **Enhanced Data Integration**: Real-time financial feeds and alternative data sources
- [ ] **Backtesting Engine**: Historical performance analysis and strategy optimization
- [ ] **Web Dashboard**: Interactive portfolio monitoring and agent insights
- [ ] **Multi-Asset Support**: Expand beyond equities to bonds, commodities, crypto
- [ ] **Machine Learning**: Adaptive agent weights based on historical performance
- [ ] **Paper Trading**: Simulated trading environment for strategy validation

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Disclaimer

**This software is for educational purposes only.** It does not provide investment advice and should not be used for real trading without proper due diligence. Past performance does not guarantee future results. Always consult with qualified financial advisors before making investment decisions.

## License

MIT License - see LICENSE file for details.
