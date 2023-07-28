import argparse
import logging
import json
import os

from environs import Env
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    default_file_path = os.path.join(os.getcwd(), 'new_intent.json')
    parser = argparse.ArgumentParser(description='Запуск скрипта')
    parser.add_argument(
        '-fp',
        '--file_path',
        help='Укажите путь к файлу',
        nargs='?', default=default_file_path, type=str
    )
    args = parser.parse_args()
    file_path = args.file_path
    with open(file_path, "r", encoding="utf-8") as file:
        file_contents = json.load(file)
    for job_intent, value in file_contents.items():
        training_phrases_parts = value["questions"]
        message_text = [value["answer"]]
        create_intent(project_id, job_intent, training_phrases_parts, message_text)


if __name__ == '__main__':
    main()