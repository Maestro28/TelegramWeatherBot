import config
import telebot
from weather import Forecast
from datetime import datetime
from telebot import types
from sqlite_reminder import DataBase

bot = telebot.TeleBot(config.TOKEN)
forecast = Forecast()


#from telegram import Update
#from telegram.ext import CallbackContext

"""
def star(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
"""

#bot.set_chat_description()

"""
import telegram_send
telegram_send.send(messages=["Wow that was easy!"])
"""

@bot.message_handler(commands="help")
def help(message):
    bot.send_message(message.chat.id, "Lets see what we have here: \n" +
                     "/start - command require to enter your city name\n" +
                     "/full_day_forecast - command will show weather information\n" +
                     "/check_wind - command uses to check a current wind characteristics\n" +
                     #"/next_days_prediction - use command for display weather in next days \n"+
                     "/set_reminder - command will help U to set a reminder\n" +
                     "/check_reminders - will show all your reminders\n" +
                     "/check_notifications - temporary option ) \n" +
                     "Also U can ask this parameters using simpe text messages for ask something, " +
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
    elif call.data != "i for i in [1,2,3]:":
        db = DataBase()
        for reminder in db.get_reminder(call.message.chat.id):
            if call.data == reminder[1]:
                db.remove_rem(reminder[1])
        db.close()
        bot.send_message(call.message.chat.id, "Reminder removed. Try /check_reminders again")
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

@bot.message_handler(commands="check_notifications")
def check_notifications(message):
    # temporary command should be used after start
    db = DataBase()
    for reminder in db.get_reminder(message.chat.id):
        if reminder[1][0] == "t":
            if reminder[1][1] == ">":
                bot.send_message(message.chat.id, "Temperature must be HAIR then " +
                                 reminder[1][2:])
            elif reminder[1][1] == "<":
                bot.send_message(message.chat.id, "Temperature must be LOWER then " +
                                 reminder[1][2:])
        elif reminder[1][0] == "w":
            if reminder[1][1] == ">":
                bot.send_message(message.chat.id, "Wind must be HAIR then " +
                                 reminder[1][2:])
            elif reminder[1][1] == "<":
                bot.send_message(message.chat.id, "Wind must be LOWER then " +
                                 reminder[1][2:])
        elif reminder[1][0] == "h":
            if reminder[1][1] == ">":
                bot.send_message(message.chat.id, "Humidity must be HAIR then " +
                                 reminder[1][2:])
            elif reminder[1][1] == "<":
                bot.send_message(message.chat.id, "Humidity must be LOWER then " +
                                 reminder[1][2:])
        elif reminder[1] == "snow":
            bot.send_message(message.chat.id, "It must be SNOW to remind")
        elif reminder[1] == "rain":
            bot.send_message(message.chat.id, "It must be RAIN to remind")
        elif reminder[1] == "clouds":
            bot.send_message(message.chat.id, "It must be CLOUDS to remind")


    db.close()

@bot.message_handler(commands="set_reminder")
def set_reminder(message):
    if forecast.city == "x":
        bot.send_message(message.chat.id, "Oh, U Should /start at first )")
    else:
        markap_KBoard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        tempPlas = types.KeyboardButton("Temperature > X °C")
        tempMinus = types.KeyboardButton("Temperature < X °C")
        windPlas = types.KeyboardButton("Wind speed > X m/s")
        windMinus = types.KeyboardButton("Wind speed < X m/s")
        humPlas = types.KeyboardButton("Humidity > X %")
        humpMinus = types.KeyboardButton("Humidity < X %")
        snow = types.KeyboardButton("Snow reminder")
        rain = types.KeyboardButton("Rain reminder")
        clouds = types.KeyboardButton("Clouds reminder")

        markap_KBoard.row(tempPlas, tempMinus, snow)
        markap_KBoard.row(windPlas, windMinus, rain)
        markap_KBoard.row(humPlas, humpMinus, clouds)

        bot.send_message(message.chat.id, "Please, select reminder parameter", reply_markup=markap_KBoard)

@bot.message_handler(commands="check_reminders")
def check_reminders(message):
    db = DataBase()
    #Should add buttons to delete reminders
    markap_inline = types.InlineKeyboardMarkup()
    for reminder in db.get_reminder(message.chat.id):
        markap_inline.add(types.InlineKeyboardButton(text=reminder[1], callback_data=reminder[1]))

    bot.send_message(message.chat.id, "This is your current reminders:\n" +
                     "(U can press to delete)\n", reply_markup=markap_inline)

    db.close()



@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Function name doesn't even matter
    if "alloha" in message.text.lower():
        bot.send_message(message.chat.id, "Hola, " + message.chat.first_name +" )")

    elif "Temperature > X °C" in message.text:
        bot.send_message(message.chat.id, "Enter X as temperature to remind")
        bot.register_next_step_handler(message, create_reminder, par="t>",
                                       msg="Temperature >", sign=" °C")
    elif "Temperature < X °C" in message.text:
        bot.send_message(message.chat.id, "Enter X as temperature to remind")
        bot.register_next_step_handler(message, create_reminder, par="t<",
                                       msg="Temperature <", sign=" °C")
    elif "Wind speed > X" in message.text:
        bot.send_message(message.chat.id, "Enter X as wind speed to remind")
        bot.register_next_step_handler(message, create_reminder, par="w>",
                                       msg="Wind speed >", sign=" m/s")
    elif "Wind speed < X" in message.text:
        bot.send_message(message.chat.id, "Enter X as wind speed to remind")
        bot.register_next_step_handler(message, create_reminder, par="w<",
                                       msg="Wind speed <", sign=" m/s")
    elif "Humidity > X %" in message.text:
        bot.send_message(message.chat.id, "Enter X as humidity to remind")
        bot.register_next_step_handler(message, create_reminder, par="h>",
                                       msg="Humidity >", sign=" %")
    elif "Humidity < X %" in message.text:
        bot.send_message(message.chat.id, "Enter X as humidity to remind")
        bot.register_next_step_handler(message, create_reminder, par="h<",
                                       msg="Humidity <", sign=" %")
    elif "Snow reminder" in message.text:
        bot.send_message(message.chat.id, "Are U want me to remind U when it is snowing ?")
        bot.register_next_step_handler(message, create_simple_rem, par="snow")
    elif "Rain reminder" in message.text:
        bot.send_message(message.chat.id, "Are U want me to remind U when it is raining ?")
        bot.register_next_step_handler(message, create_simple_rem, par="rain")
    elif "Clouds reminder" in message.text:
        bot.send_message(message.chat.id, "Are U want me to remind U when it is clouds ?")
        bot.register_next_step_handler(message, create_simple_rem, par="clouds")

    elif 'wind' in message.text.lower():
        check_wind(message)
    elif 'forecast' in message.text.lower():
        full_day_forecast(message)
    else:
        bot.send_message(message.chat.id, message.text)

def create_reminder(message, par, msg, sign):
    try:
        float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Not correct format :(\n"+
                         "It should be a number. Please try next time.")
    else:
        #sqlite_reminder.set_reminder(message.chat.id, par+message.text, datetime.utcnow())
        db = DataBase()
        creatingFlag = True
        for reminder in db.get_reminder(message.chat.id):
            if reminder[1] == par+message.text:
                creatingFlag = False
        if creatingFlag:
            db.set_reminder(message.chat.id, par+message.text, datetime.utcnow())
            bot.send_message(message.chat.id, "Will remind when: " + msg + message.text +
                             sign + "\n" + "(U can /check_reminders)")
        else:
            bot.send_message(message.chat.id, "U already have that one )")
        db.close()

def create_simple_rem(message, par):
    db = DataBase()
    creatinFlag = True
    for reminder in db.get_reminder(message.chat.id):
        if reminder[1] == par:
            creatinFlag = False
    if creatinFlag:
        db.set_reminder(message.chat.id, par, datetime.utcnow())
        db.close()
        bot.send_message(message.chat.id, "Reminder created! \n"
                                          "(U can /check-reminders)")
    else:
        bot.send_message(message.chat.id, "U already have that one )")

bot.polling(none_stop=True)
