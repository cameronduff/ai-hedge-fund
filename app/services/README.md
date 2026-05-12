# 🛎️ Services Directory

This directory is intended for standalone business logic and background services that operate outside the immediate agent loop.

## 📂 Role

Services typically handle tasks that are deterministic or require long-running processes, such as scheduled portfolio rebalancing, data persistence, or complex multi-step execution logic that shouldn't be handled directly by a tool or an agent.

## 🛠️ Available Services

### 📊 Watchlist Service (`watchlist_service.py`)
The `WatchlistService` is responsible for managing the stock watchlist and performing financial analysis on specific tickers. It integrates with both `Trading212Client` and `YFinanceClient`.

**Key Capabilities:**
- **Portfolio Tracking:** Retrieves currently held positions and pending orders from Trading212.
- **Technical Indicators:** Calculates Relative Strength Index (RSI) and Moving Average Deviation.
- **Fundamental Analysis:** Fetches P/E ratios, Debt-to-Equity (D/E) ratios, and quarterly revenue growth.
- **Analyst Sentiment:** Calculates potential upside based on mean analyst price targets.
- **Earnings Monitoring:** Tracks the number of days until the next scheduled earnings report.

This service is used to provide quants and investors with the necessary data to make informed trading decisions based on predefined targets (e.g., P/E < 35, RSI 30-70).
