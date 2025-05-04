FROM python:3.11-slim

WORKDIR /app

# Установка необходимых пакетов
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов проекта
COPY . .

# Создание скрипта для проверки .env файла
RUN echo '#!/bin/bash\n\
if [ ! -f .env ]; then\n\
    echo "Error: .env file not found!"\n\
    echo "Please create a .env file with the following variables:"\n\
    echo "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here"\n\
    echo "OPENAI_API_KEY=your_openai_api_key_here"\n\
    echo "LLM_SYSTEM_PROMPT=You are a helpful assistant. (optional)"\n\
    echo "\nYou can copy env.example and fill in your values:"\n\
    echo "cp env.example .env"\n\
    exit 1\n\
fi\n\
\n\
python ChatGPTInlineBot.py' > /app/entrypoint.sh && \
chmod +x /app/entrypoint.sh

# Запуск бота через entrypoint скрипт
CMD ["/app/entrypoint.sh"] 