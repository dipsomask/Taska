import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
import join
from num2words import num2words
import webbrowser


def respond(voice: str):
    print(voice)
    parts = voice.replace('"', ' ')
    parts = parts.replace(':', ' ').split(' ')
    part8 = parts[8]
    if part8 in config.name:
        cmd = recognize_cmd(filter_cmd(voice))
        part9 = parts[9]
        if part9 in config.cmdkom["browser"]:
            cmd = 'browser'
            parts = (" ".join(parts[9:-1]))
            execute_cmd(cmd, parts)
        elif cmd['cmd'] in config.cmdkom.keys():
            execute_cmd(cmd['cmd'], voice)
        else:
            text = "Я вас не понимаю!!!"
            tts.speak(text)


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.name:
        cmd = cmd.replace(x, "").strip()

    for x in config.tbr:
        cmd = cmd.replace(x, "").strip()

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
        text = text.replace(" ", "+")
        url = "https://yandex.ru/search/?text=" + text + "&lr=67"
        webbrowser.open_new(url)