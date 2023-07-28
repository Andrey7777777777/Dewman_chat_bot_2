import logging

import telegram
from environs import Env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dialogflow import detect_intent_texts
from log_handler import TelegramLogsHandler


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствейте")


def get_answer(update, context):
    client_text = [update.message.text]
    session_id = update.effective_chat.id
    language_code = 'ru'
    project_id = context.bot_data['project_id']
    ai_answer = detect_intent_texts(project_id, session_id, client_text, language_code).fulfillment_text
    update.message.reply_text(ai_answer)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='tg_bot.log'
        )
    logger.setLevel(logging.DEBUG)
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    bot_token = env.str('TELEGRAM_TOKEN')
    tg_chat_id = env.str('TG_CHAT_ID')
    bot = telegram.Bot(token=bot_token)
    try:
        updater = Updater(bot_token)
        dispatcher = updater.dispatcher
        bot_data = {
            "project_id": project_id
        }
        logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))
        logger.info('Бот запущен')
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text, get_answer))
        dispatcher.bot_data = bot_data
        updater.start_polling()
        updater.idle()
    except Exception as error:
        logger.exception(f'tg_bot упал с ошибкой: {error}')


if __name__ == '__main__':
    main()