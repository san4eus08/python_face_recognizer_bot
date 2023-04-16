from deepface import DeepFace
import json
import telebot
import requests
import os


def face_analyze(url):
    try:
        file_name, file_ext = os.path.splitext(url)
        respose = requests.get(url)
        open(f"{file_name[-5:-4]}{file_ext}", "wb").write(respose.content)

        result_dict = DeepFace.analyze(img_path=f'{file_name[-5:-4]}{file_ext}', actions=["age", 'gender', 'race', 'emotion'])
        with open('face_analyze.json', 'w') as file:
            json.dump(result_dict, file, indent=4, ensure_ascii=False)
        os.remove(f"{file_name[-5:-4]}{file_ext}")
        return f'age: {result_dict[0]["age"]}, gender: {result_dict[0]["dominant_gender"]}, race: {result_dict[0]["dominant_race"]}, emotion: {result_dict[0]["dominant_emotion"]}'

    except Exception as ex:
        return ex


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Hello")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if 'analyze' in message.text.lower().split():
            url = message.text.lower().split()[-1]
            print(url)
            try:
                bot.send_message(message.chat.id, face_analyze(url))
                print(face_analyze(url))
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, f"Something went wrong... {ex}")

    bot.polling()


def main():
    telegram_bot("5921225699:AAEISTdf9egJ-fk0t4E15AYXxiz_h8C6O90")


if __name__ == "__main__":
    main()
