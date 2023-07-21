from google.cloud import dialogflow
import logging

from environs import Env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        return response.query_result.fulfillment_text


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствейте")


def get_answer(update, context):
    client_text = [update.message.text]
    session_id = update.effective_chat.id
    language_code = 'ru'
    project_id = context.bot_data['project_id']
    ai_answer = detect_intent_texts(project_id, session_id, client_text, language_code)
    update.message.reply_text(ai_answer)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    bot_token = env.str('TELEGRAM_TOKEN')
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    bot_data = {
        "project_id": project_id,
    }
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, get_answer))
    dispatcher.bot_data = bot_data

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()