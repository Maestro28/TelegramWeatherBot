import time
import schedule
import bot

schedule.every(10).seconds.do(bot.make_notification())


while True:
    schedule.run_pending()
    time.sleep(1)