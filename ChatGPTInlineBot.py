import os
from dotenv import load_dotenv
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, InlineQueryHandler, ContextTypes
import logging
import uuid
import httpx
import re

# Загрузка переменных окружения из .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_HTTP_REFERER = os.getenv("OPENROUTER_HTTP_REFERER")
OPENROUTER_APP_TITLE = os.getenv("OPENROUTER_APP_TITLE")
LLM_SYSTEM_PROMPT = os.getenv("LLM_SYSTEM_PROMPT", "You are a helpful assistant.")

# Логирование для отладки
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Минимальная длина запроса
MIN_QUERY_LENGTH = 10
MAX_QUERY_LENGTH = 200

# Для хранения последних запросов пользователей
last_queries = {}

def is_english(text):
    # Если больше половины символов — латиница, считаем английским
    letters = re.findall(r'[a-zA-Z]', text)
    return len(letters) > len(text) / 2

async def ask_openrouter(prompt: str) -> str:
    logger.info(f"Запрос к OpenRouter: {prompt}")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    if OPENROUTER_HTTP_REFERER:
        headers["HTTP-Referer"] = OPENROUTER_HTTP_REFERER
    if OPENROUTER_APP_TITLE:
        headers["X-Title"] = OPENROUTER_APP_TITLE

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": LLM_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        logger.info(f"Ответ от OpenRouter: {result}")
        return result["choices"][0]["message"]["content"].strip()

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    user_id = update.inline_query.from_user.id
    logger.info(f"Получен inline-запрос от пользователя {user_id}: '{query}'")
    results = []

    if len(query) < MIN_QUERY_LENGTH:
        logger.info(f"Запрос слишком короткий: '{query}'")
        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Request too short",
                input_message_content=InputTextMessageContent("Request too short. Please enter a longer prompt."),
                description="Minimum 10 characters"
            )
        )
        await update.inline_query.answer(results, cache_time=1)
        return

    if len(query) > MAX_QUERY_LENGTH:
        logger.info(f"Запрос слишком длинный: '{query}'")
        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Request too long",
                input_message_content=InputTextMessageContent(f"Request too long. Please shorten your prompt (max {MAX_QUERY_LENGTH} characters)."),
                description=f"Maximum {MAX_QUERY_LENGTH} characters"
            )
        )
        await update.inline_query.answer(results, cache_time=1)
        return

    # Получаем ответ от OpenRouter
    try:
        answer = await ask_openrouter(query)
    except Exception as e:
        logger.error(f"OpenRouter error: {e}")
        answer = "Error contacting OpenRouter."

    # Формируем ответ с текстом запроса (сначала ответ, затем вопрос)
    if is_english(query):
        answer_label = "Answer"
        query_label = "Your query"
    else:
        answer_label = "Ответ"
        query_label = "Ваш запрос"

    full_answer = f"{answer_label}: {answer}\n\n{query_label}: {query}"

    # Отправляем реальный ответ
    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="ChatGPT",
            input_message_content=InputTextMessageContent(full_answer),
            description=full_answer[:100]  # Краткое описание
        )
    ]
    logger.info(f"Отправляю ответ пользователю {user_id}: {full_answer}")
    await update.inline_query.answer(results, cache_time=1)

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(InlineQueryHandler(inline_query_handler))
    application.run_polling()

if __name__ == "__main__":
    main()
