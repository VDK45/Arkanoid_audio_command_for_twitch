import config
import urllib.request as urllib2
import json
import time
# import thread
from time import sleep


def mess(sock, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(config.CHAN, message).encode())



