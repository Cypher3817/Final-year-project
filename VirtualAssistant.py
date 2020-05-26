import os
import re
import sys
import webbrowser
from time import strftime
import requests
import speech_recognition as sr
from pyowm import OWM


def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand()
    return command


def sofiaResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
        os.system('say ' + audio)

sofiaResponse('Hi User, I am Sophia and I am your personal voice assistant, Please give a command or say "help me" and '
              'I will tell you what all I can do for you.')


def assistant(command):
    "if statements for executing commands"
    # open subreddit Reddit
    if 'open reddit' in command:
        regex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if regex:
            subreddit = regex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        sofiaResponse('The Reddit content has been opened for you Sir.')
    # Shutdown
    elif 'shut down' in command:
        sofiaResponse('Bye bye. Have a nice day')
        sys.exit()

    # open website
    elif 'open' in command:
        regex = re.search('open (.+)', command)
        if regex:
            domain = regex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            sofiaResponse('The website you have requested has been opened for you.')
        else:
            pass

    # greetings
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            sofiaResponse('Hello. Good morning')
        elif 12 <= day_time < 18:
            sofiaResponse('Hello. Good afternoon')
        else:
            sofiaResponse('Hello. Good evening')
    # Help
    elif 'help me' in command:
        sofiaResponse("""
        You can use these commands and I'll help you out:
        1. Open reddit subreddit : Opens the subreddit in default browser.
        2. Open xyz.com : replace xyz with any website name
        3. Current weather in {cityname} : Tells you the current condition and temperture
        4. Hello
        5. time : Current system time 
        6. joke
        7. shutdown 
        """)

    # joke
    elif 'joke' in command:
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers={"Accept": "application/json"})
        if res.status_code == requests.codes.ok:
            sofiaResponse(str(res.json()['joke']))
        else:
            sofiaResponse('oops!I ran out of jokes')

    # current weather
    elif 'current weather' in command:
        regex = re.search('current weather in (.*)', command)
        if regex:
            city = regex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            sofiaResponse(
                'Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f '
                'degree celcius' % (
                    city, k, x['temp_max'], x['temp_min']))

    # time
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        sofiaResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

# loop to continue executing multiple commands
while True:
    assistant(myCommand())



