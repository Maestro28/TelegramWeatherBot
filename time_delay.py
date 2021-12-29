import time
import schedule
import bot

schedule.every(1).minutes.do(bot.make_notification())


while True:
    #time.sleep(10)
    #bot.make_notification()
    schedule.run_pending()
    time.sleep(1)