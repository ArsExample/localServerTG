import subprocess

import pyautogui


def alert(text):
    pyautogui.alert(text=text, title="Alert", button="OK")

def warning(text):
    pyautogui.alert(text=text, title="Warning", button="OK")
