# email bots 2021
# editor famz__botz
from Famzbotz.linepy1 import *
from akad.ttypes import *
from thrift.famzhttp import *
from thrift.Thrift import *
from thrift.TSerialization import *
from thrift.TMultiplexedProcessor import *
from akad.ttypes import Message
from akad.ttypes import ContentType as Type
from akad.ttypes import TalkException
from thrift.protocol import TCompactProtocol
from thrift.transport import THttpClient
from akad.ttypes import LoginRequest
from datetime import datetime, timedelta
from threading import Thread
from io import StringIO
from multiprocessing import Pool
from urllib.parse import urlencode
from random import randint
from shutil import copyfile
import subprocess as cmd
import time, random, sys, json, codecs, shutil, threading, glob, re, base64, string, os, requests, six, ast, pytz, urllib, urllib.parse, atexit, asyncio, traceback, livejson

class Bardiansyah1(object):
    def __init__(self, _id='', passwd='', type=None):
        self.famz = LINE(_id, passwd)
        print('success login bot '+str(type))
        self.oepoll = OEPoll(self.famz)
        self.mid = self.famz.getProfile().mid

        self.admin = ["you_mid"]

        self.squad = livejson.File("squad.json")
        self.asist = self.squad["asist"]
        self.bots = self.squad["bots"]

        if type != None: 
            self.type = type
        else:
            self.type = type
        if str(self.type) not in self.asist:
            self.asist[str(self.type)] = self.mid
        if self.mid not in self.bots:
            self.bots[self.mid] = True

        self.wait = {
            "keyCommand": ""
        }

        self.helpMsg = """ Famz Help
> help
> mid
> ping
> sp
"""
    def command(self, text):
        pesan = text.lower()
        if pesan.startswith(self.wait["keyCommand"]):
            cmd = pesan.replace(self.wait["keyCommand"],"")
        else:
            cmd = "command"
        return cmd

    def receive_message(self, op):
        global time
        global ast
        global groupParam
        try:
            if op.type in [25, 26]:
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                pengirim = msg._from
                if msg.toType == 0 or msg.toType == 2:
                    if msg.toType == 0:
                        to = receiver
                    if msg.toType == 2:
                        to = receiver
                if msg.contentType == 0:
                    if text is None:
                        return
                    else:
                        cmd = self.command(text)

                        if cmd == "mid":
                            self.famz.sendMessage(to, msg._from)

                        if self.type == self.type and pengirim in self.admin:

                            if cmd == "help":
                                self.famz.sendMessage(to,self.helpMsg)

                            if cmd == "ping":
                                self.famz.sendMessage(to,'pong')

                            if cmd == "sp":
                                start = time.time()
                                self.famz.getGroupWithoutMembers(to)
                                total = time.time() - start
                                self.famz.sendMessage(to,"%.10f" % (total/3))

        except Exception as error:
                print (error)
    def run1(self):
        while True:
            try:
                ops=self.oepoll.singleTrace(count=50)
                if ops != None:
                    for op in ops:
                        self.receive_message(op)
                        self.oepoll.setRevision(op.revision)
            except Exception as e:
                print(e)
