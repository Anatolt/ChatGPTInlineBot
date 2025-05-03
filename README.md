# ChatGPT Inline Telegram Bot

This is a Telegram inline bot that uses OpenAI's GPT model to answer user queries directly in any chat via inline mode.

## Features
- Inline mode: just type `@YourBotName your question` in any chat
- Uses OpenAI GPT-4-turbo for answers
- Shows both the answer and the original query
- English-only interface for all user messages
- Query length limits (min 10, max 200 characters)

## Requirements
- Python 3.8+
- Telegram bot token ([how to get one](https://core.telegram.org/bots#6-botfather))
- OpenAI API key ([how to get one](https://platform.openai.com/account/api-keys))

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ChatGPTInlineBot.git
   cd ChatGPTInlineBot
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Create a `.env` file:**
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   OPENAI_API_KEY=your_openai_api_key
   # Optional: LLM_SYSTEM_PROMPT=You are a helpful assistant.
   ```

## Usage
Run the bot:
```bash
python ChatGPTInlineBot.py
```

Add your bot to Telegram and use inline mode:
```
@YourBotName your question here
```

## Before Publishing on GitHub
- [ ] **Remove sensitive data:** Make sure `.env` and any files with secrets are in `.gitignore`.
- [ ] **Add a `.gitignore` file** (if not present):
  ```
  .env
  __pycache__/
  *.pyc
  ```
- [ ] **Check for hardcoded tokens or keys** in the code.
- [ ] **Write a short project description** in the repo (GitHub settings).
- [ ] **Add a license** (MIT, Apache 2.0, etc.) if you want others to use your code.
- [ ] **(Optional) Add usage examples/screenshots** to the README.

---

**Enjoy your ChatGPT-powered Telegram inline bot!**