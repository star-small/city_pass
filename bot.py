import telebot
import os
import json
from telebot import types
import geotools
import scrapper
API_TOKEN = '7009172269:AAG-3Jb1CVeYaQ6ub9_dWi7i4RBtCe5xNqo'
bot = telebot.TeleBot(API_TOKEN)

# Load data from file
with open("data.json", 'r', encoding='utf-8') as file:
    all_data = json.load(file)

categories = ["All", "Historical", "Architectural", "Natural", "Religious", "Museums", "Touristic", "Entertainment Centers", "Cultural"]
data = all_data  # This will be the filtered dataset according to the chosen category

# Dictionary to keep user states
user_states = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Send location", request_location=True)
    keyboard.add(button_geo)
    welcome_text = ("Welcome to the Astana Interactive Guide. Please use the commands to navigate the bot.\n"
                    "/categories to filter by category.\n"
                    "/list to list attractions based on category.\n"
                    "/help to see this message again.")
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)

@bot.message_handler(commands=['categories'])
def category_list(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    for category in categories:
        markup.add(types.KeyboardButton(text=category))
    bot.send_message(message.chat.id, "Please select a category:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in categories)
def update_data_by_category(message):
    global data
    category = message.text
    if category == "All":
        data = all_data
    else:
        data = [item for item in all_data if category in item['categories']]
    bot.send_message(message.chat.id, f"Category '{category}' selected. Use /list to see the attractions.")

@bot.message_handler(commands=['list'])
def send_list(message):
    if data:
        response_text = ""
        for i, item in enumerate(data):
            response_text += f"{i}. {item['name']}\n"
        bot.send_message(message.chat.id, response_text)
    else:
        bot.send_message(message.chat.id, "No data available. Please select a category using /categories.")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    try:
        choose = int(message.text)
        user_states[message.chat.id] = {'choose': choose}
        item = data[choose]
        name = item.get('name', 'No data')
        schedule = item.get('schedule', 'Schedule unavailable')
        contact = item.get('contact', 'Contact information not provided')
        buses_list = " ".join(item.get('buses', [])) if item.get('buses') else 'No bus routes available'
        geo = item["geo"]
        response_text = f"{name}\nSchedule: {schedule}\nAvailable bus routes: {buses_list}\nContacts: {contact}\nSend your location to build a route."
        bot.send_message(message.chat.id, response_text)
    except ValueError:
        bot.send_message(message.chat.id, "Please send a correct index number.")
    except IndexError:
        bot.send_message(message.chat.id, "Index out of range, please try a valid index.")
    except TypeError:
        bot.send_message(message.chat.id, "Data type error occurred, please try again.")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    try:
        choose = user_states[message.chat.id]['choose']
        origin = f"{message.location.latitude}, {message.location.longitude}"
        destination = f"{data[choose]['geo'][0]}, {data[choose]['geo'][1]}"
        route_url =geotools.compute_route(origin, destination)
        bot.send_photo(message.chat.id, f"{route_url}")  # Placeholder for sending the route map
        route_message = f"View route: [Google Maps](https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&travelmode=driving)"
        bot.send_message(message.chat.id, route_message, parse_mode="markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "An error occurred while processing your location: " + str(e))

bot.infinity_polling()
