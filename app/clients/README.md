# 🔌 Clients Directory

This directory contains low-level API clients for interacting with external services. These clients are responsible for handling authentication, raw HTTP requests, and basic error handling.

## 📂 Included Clients

- **`trading212_client.py`**: Handles communication with the Trading 212 API. Supports fetching account summaries, open positions, pending orders, and placing various types of orders (Market, Limit, Stop, Stop-Limit).
- **`yfinance_client.py`**: A wrapper around the `yfinance` library or direct Yahoo Finance API calls to retrieve historical market data, company info, and financial statements.

## 🛠 Usage

Clients should be instantiated once and shared or used within the `app/tools/` directory. They are designed to be "dumb" wrappers that don't contain business logic or complex state management.
