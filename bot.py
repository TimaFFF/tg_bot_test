from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот для расписания и заметок.')

def add_note(update: Update, context: CallbackContext) -> None:
    note = ' '.join(context.args)
    # Сохраняем заметку (например, в файл или базу данных)
    update.message.reply_text(f'Заметка добавлена: {note}')

def main() -> None:
    # Укажите ваш токен
    updater = Updater("7891525747:AAEZFGKnfuXgDSrR1_IVJHvrIPQ3MrdSMUY")

    dispatcher = updater.dispatcher

    # Регистрируем команды
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add_note", add_note))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("Запуск бота")
    main()
