import logging
import random
from environs import Env


import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from DialogFlow import detect_intent_texts


def get_ai_answer(event, vk_api, project_id):
    text = [event.text]
    user_id = event.user_id
    ai_answer = detect_intent_texts(project_id, user_id, text)
    vk_api.messages.send(
        user_id=event.user_id,
        message=ai_answer,
        random_id=random.randint(1,1000)
    )


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    bot_vk_token = env.str('VK_API_TOKEN')
    vk_session = vk.VkApi(token=bot_vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            get_ai_answer(event, vk_api, project_id)


if __name__ == '__main__':
    main()