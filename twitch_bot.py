import random
import config
import utils
import socket
import re
import time
from time import sleep

command = ''
message = 'Hello world!'
chater = 'VDK_45'
loop_true = True
lst_chat = ['VDK45', 'Hello world!', 'VDK45', 'TF2D', 'VDK45', 'This is my first project', 'VDK45', 'Python']
sound = False
def send_mess(x):
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))
    #chat_message = re.compile(r"^w+")
    utils.mess(s, x)



def run():
    global description
    global description2
    global description3
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))
    ##chat_message = re.compile(r"^:\w+!\w+@\w+.tmi\.twitch\.tv PRIVMSG #\w+ :")
    chat_message = re.compile(r"^w+")
    description = utils.mess(s, "Arkanoid Начинается! Вводите команды для управления" )
    description2 = utils.mess(s, "!left или  !right" )
    description
    description2
    global sound
    global command
    global message
    global chater
    global lst_chat
    global loop_true
    message = chater = ''
    lst_chat = ['VDK45', 'Hello world!', 'VDK45', 'TF2D', 'VDK45', 'This is my first project', 'VDK45', 'Python']
    
    while loop_true:
        response = s.recv(1024).decode("utf-8")
        sound = False
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("POND :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = chat_message.sub("", response).lower()
            message = message[1:]
            
            for i in message:
                try:
                    if i == "@":
                        chater = message[message.index('@')+ 1:message.index('.')]
                        message = message[message.index(':')+ 1:] 
                        if len(message) < 30:
                            lst_chat.insert(0, message)
                            lst_chat.insert(0, chater)
                        else:
                            lst_chat.insert(0, message[0:30])
                            lst_chat.insert(0, chater)
                            lst_chat.insert(0, f'-{message[30:60]}')
                            lst_chat.insert(0, chater)
                            lst_chat.pop()
                            lst_chat.pop()   
                        lst_chat.pop()
                        lst_chat.pop()
                except ValueError:
                    continue

                    
                
            print(f'{chater}: {message}')
            
            st = message.split()
            command = ''.join(st) 

            answers = ["Привет", "Хай", "Здарова", "Здравствуй", "Рад тебя видеть", "Салют", "Приветик", "Хэлло"]
            hello = ["привет", "хай", "здарова", "здравствуй", "добрыйвечер", "здравствуйте", "добрыйдень", "хэлло",
            "hi", "hello", 'privet']

            if chater != 'nightbot':
                sound = True
                sleep(0.03)
                sound = False

            if command == "!time" or command == "!время":
                named_tuple = time.localtime() # получить struct_time
                time_string = time.strftime("Дата: %d/%m/%Y, Время: %H:%M", named_tuple)
                utils.mess(s, time_string)
            if command  in hello:
                utils.mess(s, answers[random.randint(0, 7)] + ' ' +  chater + '!')
                
            if command == '!help':
                utils.mess(s, 'ARKANOID made by VDK45')
            if command == '!l':
                command = '!left'
                sleep(0.1)
                command = ''
            if command == '!r':
                command = '!right'
                sleep(0.1)
                command = ''
            if command == '!left':
                sleep(0.3)
                command = ''
            if command == '!right':
                sleep(0.3)
                command = ''
            if command == '!reset':
                sleep(0.3)
                command = ''
        
        if loop_true ==  False:
            print('Twitch bot has stopped')
            break

        sleep(1)
        


                



