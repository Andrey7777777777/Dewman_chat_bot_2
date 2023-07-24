import logging
import random

import telegram
from environs import Env


import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from DialogFlow import detect_intent_texts
from log_handler import TelegramLogsHandler


logger = logging.getLogger(__name__)


def get_ai_answer(event, vk_api, project_id, ):
    text = [event.text]
    user_id = event.user_id
    ai_answer = detect_intent_texts(project_id, user_id, text)
    if not ai_answer.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=ai_answer.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        # filename='vk_bot.log'
    )
    logger.setLevel(logging.DEBUG)
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    bot_vk_token = env.str('VK_API_TOKEN')
    bot_token = env.str('TELEGRAM_TOKEN')
    tg_chat_id = env.str('TG_CHAT_ID')
    vk_session = vk.VkApi(token=bot_vk_token)
    vk_api = vk_session.get_api()
    bot = telegram.Bot(token=bot_token)
    logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))
    logger.info('vk_bot запущен')
    try:
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                get_ai_answer(event, vk_api, project_id)
    except Exception as error:
        logging.exception(f"vk_bot упал с ошибкой: {error}")


if __name__ == '__main__':
    main()