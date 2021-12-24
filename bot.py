import config
import telebot
from weather import Forecast
from datetime import datetime
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
forecast = Forecast()

@bot.message_handler(commands="help")
def help(message):
    bot.send_message(message.chat.id, "Lets see what we have here: \n" +
                     "/start - command require to enter your city name\n" +
                     "/full_day_forecast - command will show weather information\n" +
                     "/check_wind - command uses to check a current wind characteristics\n" +
                     #"/next_days_prediction - use command for display weather in next days \n"
                     "Also U can ask this parameters using simpe text messages for ask something, "+
                     "with using keywords as: (wind), (forecast) etc."
                     )

@bot.message_handler(commands="start")
def start(message):
    msg = bot.send_message(message.chat.id, "Hello, " + message.chat.first_name +" )\n" +
                     "Let me know where are U 🤔\n" +
                     "Please enter the name of your city")
    bot.register_next_step_handler(msg, define_city)

def define_city(message):
        forecast.set_city(message.text)
        try:
            weather = str(forecast.get_data()["weather"][0]["main"])
        except KeyError:
            bot.send_message(message.chat.id, "Oh i can't recognize the city name\n" +
            "Please /start again")
            return None

        if "clouds" in weather.lower():
            #bot.send_message(message.chat.id, "☁")
            sign = "☁"
        elif "snow" in weather.lower():
            #bot.send_message(message.chat.id, "❄")
            sign = "❄"
        elif "clear" in weather.lower():
            #bot.send_message(message.chat.id, "☀")
            sign = "☀"
        elif "rain" in weather.lower():
            #bot.send_message(message.chat.id, "🌧")
            sign = "🌧"
        else:
            sign = "🌤"

        markap_KBoard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        helpBTN = types.KeyboardButton("/help")
        markap_KBoard.add(helpBTN)

        bot.send_message(message.chat.id, sign, reply_markup=markap_KBoard)

        #bot.send_message(message.chat.id, "Oh, it is " + weather + " outside.")
        #enter buttons
        markap_inline = types.InlineKeyboardMarkup()
        check_temp = types.InlineKeyboardButton(text="Check Temperature", callback_data="checkT")
        markap_inline.add(check_temp)

        bot.send_message(message.chat.id, "Oh, it is " + weather + " outside.", reply_markup=markap_inline)

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == "checkT":
        bot.send_message(call.message.chat.id, "Temperature: " +
                         str(forecast.get_data()['main']['temp']) + "°C\n" +
                         "Feels like: " + str(forecast.get_data()['main']['feels_like']) + "°C")
    else:
        bot.send_message(call.message.chat.id, "Something wrong :(")
    bot.answer_callback_query(callback_query_id=call.id)

@bot.message_handler(commands="full_day_forecast")
def full_day_forecast(message):
    if forecast.city == "x":
        bot.send_message(message.chat.id, "Oh, U Should /start at first )")
    else:
        bot.send_message(message.chat.id, "Weather in "
                         + str(forecast.city) +" ("+str(forecast.get_data()['sys']['country'])+")\n" +
                         "Date " + str(datetime.fromtimestamp(forecast.get_data()['dt']).strftime('%d-%m-%Y, checking time: %H:%M:%S')) + "\n" +
                         "Minimal temperature: " + str(forecast.get_data()['main']['temp_min']) + "°C\n" +
                         "Maximal temperature: " + str(forecast.get_data()['main']['temp_max']) + "°C\n" +
                         "Humidity: " + str(forecast.get_data()['main']['humidity']) + "%\n" +
                         "Sunrise time: " + str(datetime.fromtimestamp(forecast.get_data()['sys']['sunrise']).strftime('%H:%M:%S')) + "\n" +
                         "Sunset time: " + str(datetime.fromtimestamp(forecast.get_data()['sys']['sunset']).strftime('%H:%M:%S')) + "\n"
                         )

@bot.message_handler(commands="check_wind")
def check_wind(message):
    if forecast.city == "x":
        bot.send_message(message.chat.id, "Oh, U Should /start at first )")
    else:
        bot.send_message(message.chat.id, "Current wind:\n" +
                         "Wind speed: " + str(forecast.get_data()["wind"]["speed"]) + "\n" +
                         "Wind degree: " + str(forecast.get_data()["wind"]["deg"]))



@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Function name doesn't even matter
    if "alloha" in message.text.lower():
        bot.send_message(message.chat.id, "Hola, " + message.chat.first_name +" )")
    elif 'wind' in message.text.lower():
        check_wind(message)
    elif 'forecast' in message.text.lower():
        full_day_forecast(message)
    else:
        bot.send_message(message.chat.id, message.text)

bot.polling(none_stop=True)