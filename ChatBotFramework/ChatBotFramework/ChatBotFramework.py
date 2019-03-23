from telegram.ext import Updater, CommandHandler # import modules
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import Config

TOKEN = Config.token #WEBLOCTEST_BOT TOKEN KEY

def check_id(bot, update):
    print(update)

    try:
        id = update.message.chat.id
        return id
    except:
        id = update.channel_post.chat.id
        return id

def check_nickname(bot, update):
    try:
        nickname = update.message.from_user.first_name
        return nickname
    except:
        nickname = update.channel_post.from_user.first_name
        return nickname

def check_args(bot, update):
    try:
        text = update.message.text
        args = text.split(" ")
        args.remove(args[0])
        return args
    except:
        text = update.channel_post.text
        args = text.split(" ")
        args.remove(args[0])
        return args

def url_encode(string):
    utf8 = string.encode("UTF-8")
    hexUtf8 = utf8.hex()
    urlString = ""

    for i in range(len(hexUtf8)):
        if i % 2 == 0:
            urlString += "%"
        urlString += hexUtf8[i]
    return urlString

def start_command(bot, update):
    id = check_id(bot, update)
    nickname = check_nickname(bot, update)
    bot.send_message(chat_id=id, text="안녕하세요 " + nickname +"! 새로운 챗봇입니다!\n\n")

def news_command(bot, update):
    id = check_id(bot, update)
    nickname = check_nickname(bot, update)

    url = "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=105"
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response,'html.parser')
    results = soup.select("#main_content > div > div._persist > div > div > div.cluster_body > ul > li > div.cluster_text > a")

    for result in results:
        msg = ""
        msg += result.string + "\n"
        msg += result.get('href') + "\n"
        bot.send_message(chat_id = id, text = msg)


def media_command(bot, update):
    id = check_id(bot, update)
    nickname = check_nickname(bot, update)
    args = check_args(bot, update)

    if not args:
        bot.send_message(chat_id = id, text = "미디어 제목을 입력해 주세요. ex) /media [미디어 제목]")
        return

    mediaName = " ".join(args)
    mediaName = url_encode(mediaName)

    url = "https://torrentwal.com/bbs/s.php?k=" + mediaName + "&q="
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response,'html.parser')
    results = soup.select("#blist > table > tr > td.subject > a:nth-child(2)")
    
    count = 1
    msg = ""
    for result in results:
        if count == Config.mediaOutputCount + 1:
            break
        msg += str(count) + ". " + result.string.strip() + "\n"
        count+=1 
    bot.send_message(chat_id = id, text = msg)

print("[main] start")
updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start_command))
updater.dispatcher.add_handler(CommandHandler('news', news_command))
updater.dispatcher.add_handler(CommandHandler('media', media_command))

print("[main] start polling")
updater.start_polling(poll_interval=0.0,
                          timeout=10,
                          clean=False,
                          bootstrap_retries=0)
updater.idle()