from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from aiohttp import web
import json
import asyncio

# Загрузка заметок из файла
def load_notes() -> dict:
    try:
        with open("notes.json", "r") as file:
            notes = json.load(file)
            print("Заметки загружены из файла:", notes)  # Вывод в консоль
            return notes
    except FileNotFoundError:
        print("Файл с заметками не найден. Создан новый словарь.")  # Вывод в консоль
        return {}

# Сохранение заметок в файл
def save_notes(notes: dict) -> None:
    with open("notes.json", "w") as file:
        json.dump(notes, file)
        print("Заметки сохранены в файл:", notes)  # Вывод в консоль

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Бот запущен и готов к работе!")  # Вывод в консоль
    # Создаем клавиатуру с кнопками
    keyboard = [["Добавить заметку", "Показать заметки"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Привет! Я бот для управления заметками. Выберите действие:",
        reply_markup=reply_markup,
    )

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    user_id = str(update.message.from_user.id)
    print(f"Получено сообщение от пользователя {user_id}: {text}")  # Вывод в консоль

    if text == "Добавить заметку":
        await update.message.reply_text("Введите текст заметки:")
        context.user_data["awaiting_note"] = True  # Указываем, что ожидаем заметку
    elif text == "Показать заметки":
        notes = load_notes()
        if user_id in notes and notes[user_id]:
            await update.message.reply_text("Ваши заметки:\n" + "\n".join(notes[user_id]))
        else:
            await update.message.reply_text("У вас пока нет заметок.")
    elif context.user_data.get("awaiting_note"):
        # Если ожидаем заметку, сохраняем ее
        notes = load_notes()
        if user_id not in notes:
            notes[user_id] = []
        notes[user_id].append(text)
        save_notes(notes)

        await update.message.reply_text(f"Заметка добавлена: {text}")
        context.user_data["awaiting_note"] = False  # Сбрасываем флаг
    else:
        await update.message.reply_text("Используйте кнопки для управления.")

# Фиктивный HTTP-сервер
async def handle_http_request(request):
    return web.Response(text="Hello, I'm a Telegram bot!")

async def start_http_server():
    app = web.Application()
    app.router.add_get('/', handle_http_request)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)  # Слушаем порт 8080
    await site.start()
    print("HTTP-сервер запущен на порту 8080")  # Вывод в консоль

# Основная функция
async def main():
    print("Запуск бота...")  # Вывод в консоль
    # Запуск HTTP-сервера
    await start_http_server()

    # Запуск Telegram-бота
    token = "7891525747:AAEZFGKnfuXgDSrR1_IVJHvrIPQ3MrdSMUY"
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await application.run_polling()

if __name__ == '__main__':
    print("Инициализация бота...")  # Вывод в консоль
    asyncio.run(main())
