from telegram.ext import Updater
from telegram.ext import CommandHandler
from pprint import pprint as pp
import requests
from conf import *


API_URL = ('http://api.openweathermap.org/data/2.5/weather?q={}&mode=json&units=metric&appid={}')


def query_api(city):
    try:
        print(API_URL.format(city, API_KEY))
        data = requests.get(API_URL.format(city, API_KEY)).json()
    except Exception as exc:
        print(exc)
        data = None
    return data

def start(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="To start type /pogoda city_name and check the weather")

def weather_check(bot, update, args):
    try:
        user_says = " ".join(args)
        resp = query_api(user_says)
        pp(resp)
        chat_id = update.message.chat_id
        temp = int(round((resp['main']['temp'])))
        pressure = resp['main']['pressure']
        country = resp['sys']['country']
        desc = resp['weather'][0]['description']
        resp = ("Current temperature in %s, %s is %s C. \nAtmospheric pressure %s hPa\n%s" % (user_says, country, temp, pressure, desc.capitalize()))
        bot.send_message(chat_id=chat_id, text=resp)
    except KeyError:
        resp = ("City not found. We do not have weather data for %s. Please try agin using different city. " % user_says)
        bot.send_message(chat_id=chat_id, text=resp)


def main():
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('weather',weather_check, pass_args=True))

    updater.start_polling()
    updater.idle()




if __name__ == '__main__':
    main()