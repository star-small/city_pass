#!/usr/bin/python
import geotools
import scrapper
import os
import json
from telebot import types
# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot

API_TOKEN = '7009172269:AAG-3Jb1CVeYaQ6ub9_dWi7i4RBtCe5xNqo'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
user_choose = 0
with open("/home/troy/dev/gdc/data.json", 'r', encoding='utf-8') as file:
    data = json.load(file)
# print(data)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(
        text="Send location", request_location=True)
    keyboard.add(button_geo)
    text = "Я ваш интерактивный гид, призванный сделать ваш визит в Астану незабываемым. Независимо от того, ищете ли вы индивидуальное путешествие по самым потрясающим достопримечательностям города или вам нужна информация о достопримечательностях Астаны, я здесь, чтобы помочь.\nВот что я могу для вас сделать: \n✅ Создавайте персонализированные маршруты в зависимости от вашего местоположения, предпочтений и вида транспорта.\n✅ Предоставьте подробную информацию о достопримечательностях, включая описания, исторический контекст, часы работы и информацию о билетах.\n✅ Помогайте с запросами, связанными с Citypass Astana, чтобы путешествие прошло без осложнений.\nДавайте исследуем Астану вместе.! 🚀\n/list /help"
    bot.send_message(message.chat.id, text)
@bot.message_handler(commands=['update'])
def update(message):
    bot.send_message(message.chat.id, "in process")
    scrapper.dump_data()
    bot.send_message(message.chat.id, "done")


@ bot.message_handler(commands=['list'])
def send_list(message):
    if os.path.exists("/home/troy/dev/gdc/data.json"):
        text= ""
        for i in range(len(data)):
            text += str(i) + ". " + data[i]["name"] + "\n"
        bot.send_message(message.chat.id, text)
    else:
        scrapper.dump_data()
        bot.send_message(message.chat.id, "Подождите....")
        bot.send_message(message.chat.id, "Готово! Попробуйте ещё раз")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])


user_states= {}


@ bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:
        choose= int(message.text)
        user_states[message.chat.id]= {'choose': choose}
        print(choose)
        item= data[choose]
        name= item.get('name', 'Нет данных')
        schedule= item.get('schedule', 'Расписание не доступно')
        contact= item.get('contact', 'Контактная информация не предоставлена')
        buses_list= " ".join(item.get('buses', [])) if item.get(
            'buses') else 'Маршрутки не доступны'
        geo = item["geo"]
        response_text = f"{name}\nРасписание: {schedule}\nДоступные маршрутки: {buses_list}\nКонтакты: {contact}\nОтправьте свою геолокацию, чтоб я мог построить маршрут"
        bot.send_message(message.chat.id, response_text)

        @bot.message_handler(content_types=['location'])
        def handle_location(message):
            choose = user_states[message.chat.id]['choose']
            print(data[choose]["geo"], choose)
            origin = f"{message.location.latitude}, {message.location.longitude}"
            destination = f"{data[choose]['geo'][0]}, {data[choose]['geo'][1]}"
            print(destination)
            route_url = geotools.compute_route(
                origin, destination)
            bot.send_photo(message.chat.id, f"{route_url}")
            route_message = f"[посмотреть](https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&travelmode=driving)"
            bot.send_message(message.chat.id, route_message,
                             parse_mode="markdown")

    except ValueError:
        bot.send_message(
            message.chat.id, "Пожалуйста, отправьте корректный номер.")
    except TypeError:
        bot.send_message(
            message.chat.id, "Произошла ошибка типа данных, попробуйте еще раз.")


bot.infinity_polling()
bot.infinity_polling()
bot.infinity_polling()
bot.infinity_polling()
