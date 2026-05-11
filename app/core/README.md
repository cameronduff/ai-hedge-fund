# ⚙️ Core Directory

This directory contains the essential configuration and foundational components of the AI Hedge Fund application.

## 📂 Key Files

- **`config.py`**: Manages environment variables and application settings using `pydantic-settings`. This includes API keys for Gemini, Trading 212, and model selections for reasoning and formatting.

## 🛠 Configuration Management

All sensitive information should be stored in a `.env.local` file (not committed to version control). The `settings` object in `config.py` serves as the single source of truth for all configuration values used throughout the application.
