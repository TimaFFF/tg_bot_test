from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот для расписания и заметок.')

# Команда /add_note
async def add_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    note = ' '.join(context.args)  # Получаем текст заметки из аргументов команды
    if note:
        # Здесь можно сохранить заметку в базу данных или файл
        await update.message.reply_text(f'Заметка добавлена: {note}')
    else:
        await update.message.reply_text('Используйте команду так: /add_note Ваш текст')

# Основная функция
def main() -> None:
    # Укажите ваш токен
    token = "7891525747:AAEZFGKnfuXgDSrR1_IVJHvrIPQ3MrdSMUY"

    # Создаем приложение
    application = Application.builder().token(token).build()

    # Регистрируем команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_note", add_note))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    print("Запуск бота")
    main()
