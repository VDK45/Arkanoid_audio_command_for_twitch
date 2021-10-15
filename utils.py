import cfg
import urllib.request as urllib2
import json
import time
# import thread
from time import sleep


try:
    file_c = open('chanel.txt', 'r', encoding='utf-8')
    CHANEL = file_c.read()
    print(f'chanel = {CHANEL}')
    file_c.close()
except IOError as err:
    print(err)

def mess(sock, message):
    global CHANEL
    sock.send("PRIVMSG #{} :{}\r\n".format(CHANEL, message).encode())



