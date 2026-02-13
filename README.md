# ChatGPT Inline Telegram Bot

Telegram inline бот, использующий ChatGPT для ответов на запросы.

## Настройка

1. Скопируйте файл `env.example` в `.env`:
```bash
cp env.example .env
```

2. Отредактируйте файл `.env` и заполните необходимые переменные:
- `TELEGRAM_BOT_TOKEN` - токен вашего бота (получите у @BotFather)
- `OPENROUTER_API_KEY` - ваш API ключ OpenRouter
- `OPENROUTER_MODEL` - опционально, модель (например `openai/gpt-4o-mini`)
- `LLM_SYSTEM_PROMPT` - опционально, системный промпт для ChatGPT

## Запуск с Docker

1. Соберите Docker образ:
```bash
docker build -t chatgpt-inline-bot .
```

2. Запустите контейнер:
```bash
docker run -d --name chatgpt-bot --env-file .env chatgpt-inline-bot
```

## Управление контейнером

- Просмотр логов: `docker logs chatgpt-bot`
- Остановка: `docker stop chatgpt-bot`
- Запуск: `docker start chatgpt-bot`
- Удаление: `docker rm chatgpt-bot`

## Использование

1. Найдите бота в Telegram
2. В любом чате введите @имя_вашего_бота и ваш запрос
3. Выберите ответ из предложенных вариантов

## Features
- Inline mode: just type `@YourBotName your question` in any chat
- Uses OpenRouter-compatible models for answers
- Shows both the answer and the original query
- English-only interface for all user messages
- Query length limits (min 10, max 200 characters)

## Requirements
- Python 3.8+
- Telegram bot token ([how to get one](https://core.telegram.org/bots#6-botfather))
- OpenRouter API key ([how to get one](https://openrouter.ai/keys))

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
   OPENROUTER_API_KEY=your_openrouter_api_key
   # Optional: OPENROUTER_MODEL=openai/gpt-4o-mini
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
