from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import json

# Загрузка заметок из файла
def load_notes() -> dict:
    try:
        with open("notes.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Сохранение заметок в файл
def save_notes(notes: dict) -> None:
    with open("notes.json", "w") as file:
        json.dump(notes, file)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот для расписания и заметок.')

# Команда /add_note
async def add_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    note = ' '.join(context.args)

    if note:
        notes = load_notes()
        if user_id not in notes:
            notes[user_id] = []
        notes[user_id].append(note)
        save_notes(notes)

        await update.message.reply_text(f'Заметка добавлена: {note}')
    else:
        await update.message.reply_text('Используйте команду так: /add_note Ваш текст')

# Команда /show_notes
async def show_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    notes = load_notes()

    if user_id in notes and notes[user_id]:
        await update.message.reply_text('Ваши заметки:\n' + '\n'.join(notes[user_id]))
    else:
        await update.message.reply_text('У вас пока нет заметок.')

# Основная функция
def main() -> None:
    # Укажите ваш токен
    token = "7891525747:AAEZFGKnfuXgDSrR1_IVJHvrIPQ3MrdSMUY"

    # Создаем приложение
    application = Application.builder().token(token).build()

    # Регистрируем команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_note", add_note))
    application.add_handler(CommandHandler("show_notes", show_notes))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
