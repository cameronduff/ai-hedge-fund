# AI Hedge Fund

An intelligent investment analysis system that combines multiple investment philosophies and analytical approaches using AI agents to generate comprehensive trading recommendations. This system simulates how a sophisticated hedge fund might analyze securities using diverse methodologies from legendary investors and modern quantitative techniques.

## Attribution

This project is based on the original work from [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund/tree/main/src). The core architecture and agent-based approach were inspired by that implementation, with additional enhancements and modifications.

> **IMPORTANT**: This project is for educational and research purposes only. It does not execute real trades automatically. Nothing here constitutes investment advice.

## System Architecture

The AI Hedge Fund operates in three distinct phases:

### 1. Research Phase (Parallel Analysis)

Five specialized research agents analyze different aspects of securities:

- **Fundamentals Agent** (Azure): Analyzes financial statements, profitability metrics, growth rates, financial health, and valuation ratios to assess company quality
- **Growth Agent** (Gemini): Evaluates growth drivers, historical growth patterns, margin expansion, insider activity, and financial stability with web research capabilities
- **Technical Agent** (Gemini): Performs quantitative analysis using trend indicators, momentum signals, mean reversion patterns, volatility metrics, and statistical analysis
- **Sentiment Agent** (Azure): Processes news articles and market sentiment to gauge public perception and potential catalysts
- **Valuation Agent** (Gemini): Conducts intrinsic value calculations using DCF models, owner earnings, EV/EBITDA, and residual income methodologies with supplemental research

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

- **Risk Manager** (Azure): Analyzes volatility patterns, correlation risks, and determines appropriate position sizing based on portfolio risk metrics
- **Portfolio Manager** (Azure): Synthesizes all agent recommendations to make final trading decisions with proper position sizing and risk controls

**Note**: Azure OpenAI is used for analytical agents requiring precise structured output, while Gemini is used for agents benefiting from web search capabilities via `google_search` tool.

## Features

### ✅ Implemented

- **Complete Multi-Agent Pipeline**: Fully functional system with research, philosophy, and execution phases
- **Multi-Provider LLM Support**: Automatic detection and switching between Azure OpenAI, OpenAI, and Google Gemini
- **Hybrid Model Architecture**: Strategic use of Azure for analytical agents and Gemini for agents requiring web search
- **Trading 212 Integration**: Complete API client with demo/live trading capabilities and CLI interface
- **Comprehensive Analysis Tools**:
  - Fundamental analysis (profitability, growth, financial health, valuation)
  - Technical analysis (trend, momentum, mean reversion, volatility indicators)
  - Sentiment analysis (news processing, sentiment scoring)
  - Valuation analysis (DCF, owner earnings, EV/EBITDA, residual income)
- **Risk Management**: Volatility-based position sizing, correlation analysis, and portfolio risk concentration assessment
- **12 Legendary Investor Agents**: Warren Buffett, Charlie Munger, Ben Graham, Peter Lynch, Phil Fisher, Bill Ackman, Michael Burry, Cathie Wood, Stanley Druckenmiller, Aswath Damodaran, Mohnish Pabrai, Rakesh Jhunjhunwala
- **Async Pipeline Execution**: Parallel processing of research and investor agents for efficiency
- **Robust Error Handling**: Retry logic with rate limiting for LLM and API failures
- **JSON Output Persistence**: Timestamped pipeline results saved to output directory
- **Model Selection Utility**: Automatic provider detection with manual override capability

### 🚧 In Development

- **Real-time Data Integration**: Enhanced financial data feeds beyond Finnhub
- **Backtesting Framework**: Historical performance analysis of agent strategies
- **Multi-ticker Batch Processing**: Portfolio-wide analysis capabilities

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

### Required Environment Variables

Create a `.env` file in the project root (see `.env.example` for a complete template).

#### Core Required Variables

These are **required** for the system to run:

```bash
# Trading 212 API (Required for portfolio context and execution)
T212_ENV=demo              # Use 'demo' for testing, 'live' for real trading
T212_API_KEY=your_key
T212_API_SECRET=your_secret

# Finnhub API (Required for financial data)
FINNHUB_API_KEY=your_key

# LLM Rate Limiting (Required)
GENAI_LLM_RPM=2           # Requests per minute for LLM calls
```

#### LLM Provider Configuration (At Least One Required)

You must configure **at least one** LLM provider. The system uses a hybrid approach:

- **Azure/OpenAI**: Used for analytical agents (fundamentals, sentiment, risk, portfolio)
- **Gemini**: Used for research agents with web search (growth, technical, valuation)

**Recommended Setup**: Configure both Azure and Gemini for full functionality.

**Option 1: Azure OpenAI** (Recommended for production)

```bash
AZURE_API_BASE=https://your-resource.cognitiveservices.azure.com
AZURE_API_KEY=your_azure_key
AZURE_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_API_VERSION=2024-12-01-preview
```

**Option 2: OpenAI**

```bash
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini  # Optional, defaults to gpt-4o-mini
```

**Option 3: Google Gemini**

```bash
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini/gemini-2.0-flash-exp  # Optional, defaults to gemini-2.0-flash-exp
```

#### Optional Configuration

```bash
# Force a specific LLM provider (overrides auto-detection)
MODEL_PREFERENCE=azure    # Options: azure, openai, gemini
```

### API Key Setup Guide

1. **Trading 212 API**:

   - Register at [Trading 212](https://www.trading212.com/)
   - Request API access through their platform
   - **Note**: Start with `demo` environment for testing

2. **Finnhub API**:

   - Sign up at [Finnhub](https://finnhub.io/)
   - Free tier available for basic financial data

3. **LLM Providers**:
   - **Azure OpenAI**: Apply for access at [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
   - **OpenAI**: Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - **Google Gemini**: Get free key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### LLM Provider Selection

The system uses a **hybrid multi-provider approach**:

#### Automatic Provider Detection

The system automatically selects providers based on configured API keys with this priority:

**Azure OpenAI > OpenAI > Gemini**

#### Agent-Specific Model Assignment

Different agents use different providers based on their needs:

| Provider         | Agents                                                                           | Reason                                              |
| ---------------- | -------------------------------------------------------------------------------- | --------------------------------------------------- |
| **Azure/OpenAI** | Fundamentals, Sentiment, Risk Manager, Portfolio Manager, All 12 Investor Agents | Precise structured output, better schema compliance |
| **Gemini**       | Growth, Technical, Valuation                                                     | Web search capabilities via `google_search` tool    |

#### Testing Your Configuration

Verify which providers are configured and what the system will use:

```bash
python test_model_selector.py
```

This shows:

- Available providers (based on API keys)
- Default provider for auto-detection
- Which model will be used

#### Manual Override

Force a specific provider by setting in `.env`:

```bash
MODEL_PREFERENCE=azure    # Force Azure for all agents (except those requiring google_search)
MODEL_PREFERENCE=openai   # Force OpenAI
MODEL_PREFERENCE=gemini   # Force Gemini
```

**Note**: Agents requiring `google_search` (Growth, Technical, Valuation) will always use Gemini regardless of `MODEL_PREFERENCE`.

### Temperature Settings

Each agent uses carefully tuned temperature settings for optimal performance:

| Agent Type        | Temperature | Reasoning                                                                             |
| ----------------- | ----------- | ------------------------------------------------------------------------------------- |
| Analytical Agents | 0.0-0.1     | Fundamentals, Sentiment, Growth, Technical, Valuation, Risk - strict schema adherence |
| Portfolio Manager | 0.5         | Balanced decision-making for strategic choices                                        |
| Investor Agents   | 0.3-0.7     | Varies by investment philosophy                                                       |

## Usage

### Running the AI Hedge Fund Pipeline

Execute the complete analysis pipeline:

```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # if not already activated

# Run the main pipeline
python main.py
```

This will:

1. Connect to Trading 212 and build portfolio context
2. Initialize all research agents (fundamentals, growth, technical, sentiment, valuation)
3. Run all 12 investor philosophy agents in parallel
4. Apply risk management and portfolio optimization
5. Generate final trading recommendations with position sizing
6. Save results to `output/pipeline_result_YYYYMMDD_HHMMSS.json`

### Output

Pipeline results are automatically saved to the `output/` directory with timestamps:

- **Success**: `output/pipeline_result_20251103_102030.json`
- **Errors**: `output/pipeline_error_20251103_102030.json`

Each output includes:

- Recommendations with tickers, exchanges, weights, and reasoning
- Proposed market actions (BUY/SELL with quantities)
- Analysis notes and justifications

### Individual Agent Testing

Test specific agents independently:

```bash
# Run fundamentals analysis
python -m src.agents.fundamentals_agent.agent

# Test Warren Buffett investment philosophy
python -m src.agents.investors.warren_buffett.agent

# Test risk manager
python -m src.agents.risk_manager.agent
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

| Agent            | Model  | Purpose                                           | Key Metrics                                            |
| ---------------- | ------ | ------------------------------------------------- | ------------------------------------------------------ |
| **Fundamentals** | Azure  | Analyzes company financial health and performance | ROE, profit margins, debt ratios, growth rates         |
| **Growth**       | Gemini | Evaluates growth drivers and sustainability       | Revenue growth, earnings growth, margin expansion      |
| **Technical**    | Gemini | Identifies price patterns and trading signals     | Moving averages, RSI, Bollinger Bands, volume analysis |
| **Sentiment**    | Azure  | Processes news and market sentiment               | News sentiment scores, article analysis, market buzz   |
| **Valuation**    | Gemini | Determines intrinsic value and fair price         | DCF models, owner earnings, EV/EBITDA, residual income |

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

| Agent                 | Model | Purpose                                     | Key Functions                                                |
| --------------------- | ----- | ------------------------------------------- | ------------------------------------------------------------ |
| **Risk Manager**      | Azure | Controls position sizing and portfolio risk | Volatility analysis, correlation assessment, position limits |
| **Portfolio Manager** | Azure | Makes final trading decisions               | Signal aggregation, position sizing, execution timing        |

## Project Structure

```
src/
├── agents/                 # All AI agents
│   ├── fundamentals_agent/ # Financial analysis (Azure)
│   ├── growth_agent/       # Growth analysis (Gemini)
│   ├── technicals_agent/   # Technical analysis (Gemini)
│   ├── sentiment_agent/    # News sentiment (Azure)
│   ├── valuation_agent/    # Intrinsic value (Gemini)
│   ├── investors/          # 12 legendary investor philosophies (Azure)
│   ├── risk_manager/       # Risk assessment (Azure)
│   ├── portfolio_manager/  # Final decisions (Azure)
│   └── retrying_agent/     # Error handling & retry logic
├── clients/                # External API clients
│   ├── FinnhubClient.py   # Financial data integration
│   └── Trading212.py      # Brokerage integration & CLI
├── tools/                  # Analysis functions for each agent
├── utils/                  # Helper utilities
│   ├── model_selector.py  # Multi-provider LLM selection
│   └── context_builder.py # Trading 212 context assembly
├── pipeline.py            # Agent orchestration and workflow
├── runner.py              # Async execution engine
└── main.py                # Entry point with output persistence
```

## Roadmap

### Planned Enhancements

- [ ] **Enhanced Data Integration**: Real-time financial feeds and alternative data sources beyond Finnhub
- [ ] **Backtesting Engine**: Historical performance analysis and strategy optimization framework
- [ ] **Multi-Asset Support**: Expand beyond equities to bonds, commodities, and cryptocurrencies
- [ ] **Machine Learning Integration**: Adaptive agent weights based on historical performance
- [ ] **Paper Trading Mode**: Simulated trading environment for strategy validation
- [ ] **Performance Analytics**: Detailed tracking of agent accuracy and portfolio returns
- [ ] **Custom Investor Agents**: Framework for creating user-defined investment philosophies

## Troubleshooting

### Common Issues

**"Model azure/gpt-4o-mini not found"**

- The `google_search` tool only works with Gemini models
- Solution: Growth, Technical, and Valuation agents are configured to use Gemini
- Ensure `GEMINI_API_KEY` is set in your `.env`

**"ValidationError: Field required" or schema validation errors**

- LLM returned incorrect output format
- Solution: Lower temperatures (0.1-0.3) improve schema compliance
- Check that you're using a compatible model (gpt-4o-mini, gemini-2.0-flash-exp)

**"Rate limit exceeded (429)"**

- Trading 212 API has rate limits
- Solution: The system automatically retries with exponential backoff
- Be patient - the pipeline may take 5-10 minutes due to API limits

**"Gemini refusing to process request"**

- Gemini may refuse financial decision-making tasks
- Solution: Agents have been updated with "research only" prompts
- Sentiment agent switched to Azure to avoid refusal issues

**Virtual environment issues**

- Always activate venv: `source .venv/bin/activate`
- Use `python main.py` not just `python` (which may use system Python)

### Debugging Tips

1. **Test model configuration**: Run `python test_model_selector.py`
2. **Check logs**: Look for ERROR/WARNING messages in terminal output
3. **Verify API keys**: Ensure all required keys are set in `.env`
4. **Start with demo**: Use `T212_ENV=demo` before live trading
5. **Check output**: Review saved JSON in `output/` directory for error details

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
