import twitch_bot as tb
import speech_recognition as sr
import os
import sys
import webbrowser
import pyttsx3
import cfg

assis = True



def talk(words):
     print(words)
     #os.system('say' + words)
     engine = pyttsx3.init()
     engine.say(words)
     engine.runAndWait()
     
#talk(f'Привет, {cfg.CHAN}')


def command_ru():
     r = sr.Recognizer()

     with sr.Microphone() as source:
          print("Говорите!")
          r.pause_threshold = 1 # ждать команды
          audio = r.listen(source)
          r.adjust_for_ambient_noise(source, duration=1) 
     try:
          phrase_ru = r.recognize_google(audio, language='ru-RU').lower()
          #print('Вы сказали: ' +  phrase)
     except sr.UnknownValueError:
          #talk('try again!')
          phrase_ru = command_ru()
     return phrase_ru


def command():
     r = sr.Recognizer()
     global assis
     if assis == False:
         print('AA Stopped')
         sys.exit()
     with sr.Microphone() as source:
          print("Говорите!")
          r.pause_threshold = 1 # ждать команды
          audio = r.listen(source)
          r.adjust_for_ambient_noise(source, duration=1) 
     try:
          phrase = r.recognize_google(audio, language='en-US').lower()
          #print('Вы сказали: ' +  phrase)
     except sr.UnknownValueError:
          #talk('try again!')
          phrase = command()
     return phrase


def actions(phrase):
     global assis
     if 'left' in phrase:
          print('Move to Left')
          tb.send_mess('!left')

     if 'right' in phrase:
          print('Move to Right')
          tb.send_mess('!right')
     
     if 'stop' in  phrase or assis == False:
          talk("ok, i stopped")
          assis = False
          sys.exit()
     else:
          print('Command: ' +  phrase)


def run():
     global assis
     while assis:
          actions(command())
          if assis == False:
            sys.exit()
            break




