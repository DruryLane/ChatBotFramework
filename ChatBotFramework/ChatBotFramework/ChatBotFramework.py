import telegram
import Config

bot = telegram.Bot(token = Config.token)
lastID = None

while True:
    updates = bot.getUpdates(lastID)
    if updates:
        for u in updates:
            print(u.message)
            bot.send_message(u.message.chat_id, text=u.message.text)
        lastID = updates[-1].update_id + 1