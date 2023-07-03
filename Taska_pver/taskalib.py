import random

import ytlinks
import config
import tts
from fuzzywuzzy import fuzz
import datetime
from num2words import num2words
import webbrowser


def playyt(search):
    first_column = [row[0] for row in ytlinks.songs]
    if search in first_column:
        index = first_column.index(search)
        url = ytlinks.songs[index][1]
    else:
        search.replace(" ", '+')
        url = "https://yandex.ru/search/?text=" + search
    webbrowser.open_new(url)


def rand_music_or_radio(text):
    if text == 'радио':
        webbrowser.open_new("https://online-red.com/radio/europa-plus.html")
    else:
        tts.speak("Включаю случайный трэк...")
        index = random.randint(0,24)
        url = ytlinks.songs[index][1]
        webbrowser.open_new(url)


def respond(voice: str):
    print(voice)
    parts = voice.replace('"', ' ')
    parts = parts.replace(':', ' ').split(' ')
    part8 = parts[8]
    if part8 in config.name:
        if part8 == parts[-2]:
            return tts.speak(random.choice(config.what))
        cmd = recognize_cmd(filter_cmd(voice))
        part9 = parts[9]
        parts10 = parts[10]
        if part9 in config.cmdkom["browser"]:
            cmd = 'browser'
            parts = ("+".join(parts[9:-1]))
            return execute_cmd(cmd, parts)
        elif (parts10 == 'музыку') or (parts10 == 'музыка') or (parts10 == 'радио'):
            return rand_music_or_radio(parts10)
        elif part9 == 'зачитай':
            cmd = 'music'
            parts = (" ".join(parts[10:-1]))
            return execute_cmd(cmd, parts)
        elif (parts10 == 'песню') or (parts10 == 'видео'):
            cmd = 'music'
            parts = (" ".join(parts[11:-1]))
            return execute_cmd(cmd, parts)
        elif cmd['cmd'] in config.cmdkom.keys():
            return execute_cmd(cmd['cmd'], voice)
        else:
            text = "Я вас не понимаю!!!"
            return tts.speak(text)


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.name:
        cmd = cmd.replace(x, "").strip()

    # for x in config.tbr:
    #    cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.cmdkom.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str, voice: str):
    if cmd == 'help':
        text = "Я личный ассистент генерального директора Дипсомаска, и я могу..."
        text += "подсказать время..."
        text += "включить музыку, чтобы к генеральному директору пришло вдохновение..."
        text += "а так же..."
        text += "как уважающий себя секретарь..."
        text += "могу найти информацию в интернете!!!"
        tts.speak(text)

    elif cmd == 'ctime':
        now = datetime.datetime.now()
        text = "В данный момент" + num2words(now.hour, lang='ru') + "часов" + \
               num2words(now.minute, lang='ru') + "минут..." + "..."
        tts.speak(text)

    elif cmd == 'browser':
        text = str(voice)
        url = "https://yandex.ru/search/?text=" + text
        webbrowser.open_new(url)

    elif cmd == 'music':
        text = str(voice)
        playyt(text)
