import psutil
import telebot
from telebot import TeleBot

# Get user's computer username
username = psutil.users()[0].name

desktop_path = "C:/Users/" + username + "/Desktop/"

# Create a txt file to store the bot token inside
token_filename = "C:/Users/" + username +"/Bot_token.txt"
f = open(token_filename,"a")
f.close()

# Read the token inside the txt file
f = open(token_filename,"r")
read_token = f.readline()
f.close()

# If the token is missing, ask the user to input it
if read_token=="":
    print("Bot token missing!\n\nInstructions:")
    print("\n1. Search @BotFather on Telegram and start the bot")
    print("2. Send the command \\newbot to the bot")
    print("3. The bot will provide you with a token: copy and paste it here")
    print("Now all you have to do is keep this program running and enjoy sending files to your computer through your bot instantly!")
    write_token = input("Insert token: ")
    ff = open(token_filename,"w")
    ff.write(write_token)
    ff.close()
    BOT_TOKEN = write_token
else:
    BOT_TOKEN = read_token

print("Files sent:")

bot = telebot.TeleBot(BOT_TOKEN)

# Handler for documents
@bot.message_handler(content_types=['document'])
def addfile(message):
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(desktop_path+file_name, "wb") as new_file:
        new_file.write(downloaded_file)
        print("New document received:",file_name)
    bot.delete_message(message.chat.id, message.id)

# Handler for images
@bot.message_handler(func=lambda m: True, content_types=['photo'])
def addimage(message):
    file_name = message.photo.pop().file_id
    file_info = bot.get_file(file_name)
    file = bot.download_file(file_info.file_path)
    with open(desktop_path+file_name+".jpg", "wb") as new_file:
        new_file.write(file)
        print("New image received:",file_name)
    bot.delete_message(message.chat.id, message.id)

bot.infinity_polling()
