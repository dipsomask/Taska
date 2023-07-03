# The main file of Taska assistant

import random
import config
import stt
import tts
import taskalib
import datetime as dt

# initialization and hallo phrase
print(f"Вы можете называть меня - {config.name}")
t = dt.datetime.now()
if 5 < t.hour < 12:
    timeday = "morning"
    tts.speak(random.choice(config.hallo[timeday]))

elif 12 < t.hour < 17:
    timeday = "day"
    tts.speak(random.choice(config.hallo[timeday]))

else:
    timeday = "evening"
    tts.speak(random.choice(config.hallo[timeday]))

#tts.speak("Я плохо проговарию свои имена, поэтому спросите их у Генерального директора, или посмотрите в конфигах!!!")

# start listening comands
stt.listen(taskalib.respond)
