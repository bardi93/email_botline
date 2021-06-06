# -*- coding: utf-8 -*-
from akad.ttypes import Message, ContactSetting, ContactType, SettingsAttribute
from random import randint
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import json, ntpath, humanize, traceback, os, subprocess
import time,random,sys,json,requests,os,subprocess,re,ast,traceback,humanize,threading,base64
def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other('You want to call the function, you must login to LINE')
    return checkLogin

class Talk(object):
    isLogin = False
    _messageReq = {}
    _unsendMessageReq = 0


    def __init__(self):
        self.isLogin = True

    """Liff"""
        
    @loggedIn
    def issueLiffView(self, request):
        return self.liff.issueLiffView(request)
        
    @loggedIn
    def revokeToken(self, request):
        return self.liff.revokeToken(request)
    """User"""

    @loggedIn
    def acquireEncryptedAccessToken(self, featureType=2):
        return self.talk.acquireEncryptedAccessToken(featureType)

    @loggedIn
    def getProfile(self):
        return self.talk.getProfile()

    @loggedIn
    def getSettings(self):
        return self.talk.getSettings()

    @loggedIn
    def getUserTicket(self):
        return self.talk.getUserTicket()

    @loggedIn
    def updateProfile(self, profileObject):
        return self.talk.updateProfile(0, profileObject)

    @loggedIn
    def updateSettings(self, settingObject):
        return self.talk.updateSettings(0, settingObject)

    @loggedIn
    def updateProfileAttribute(self, attrId, value):
        return self.talk.updateProfileAttribute(0, attrId, value)

    """Operation"""

    @loggedIn
    def fetchOperation(self, revision, count):
        return self.talk.fetchOperations(revision, count)

    @loggedIn
    def getLastOpRevision(self):
        return self.talk.getLastOpRevision()

    """Message"""
    @loggedIn
    def sendMusic(self, to, text, purl, aurl, stxt, name):
        contentMetadata = {'previewUrl': purl, 'i-installUrl': aurl, 'type': 'mt', 'subText': stxt, 'a-installUrl': aurl, 'a-installUrl': aurl, 'a-packageName': 'com.spotify.music', 'countryCode': 'ID', 'a-linkUri': aurl, 'i-linkUri': aurl, 'id': 'mt000000000a6b79f9', 'text': name, 'linkUri': aurl}
        contentType = 19
        return self.sendMessage(to, text, contentMetadata, contentType)

    @loggedIn
    def generateReplyMessage(self, relatedMessageId):
        msg = Message()
        msg.relatedMessageServiceCode = 1
        msg.messageRelationType = 3
        msg.relatedMessageId = str(relatedMessageId)
        return msg

    @loggedIn
    def sendReplyMessage(self, relatedMessageId, to, text, contentMetadata={}, contentType=0):
        msg = self.generateReplyMessage(relatedMessageId)
        msg.to = to
        msg.text = text
        msg.contentType = contentType
        msg.contentMetadata = contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    @loggedIn
    def sendReplyImage(self, matId, to, path):
        objectId = self.sendReplyMessage(matId, to=to, text=None, contentType = 1).id
        return self.uploadObjTalk(path=path, type='image', returnAs='bool', objId=objectId)

    @loggedIn
    def sendReplyVideo(self, matId, to, path):
        objectId = self.sendReplyMessage(matId, to=to, text=None, contentMetadata={'VIDLEN': '60000','DURATION': '60000'}, contentType = 2).id
        return self.uploadObjTalk(path=path, type='video', returnAs='bool', objId=objectId)

    @loggedIn
    def sendReplyVideoWithURL(self,matId, to, url):
        path = self.downloadFileURL(url, 'path')
        self.sendReplyVideo(matId, to, path)
        return self.deleteFile(path)

    @loggedIn
    def sendReplyImageWithURL(self,matId, to, url):
        path = self.downloadFileURL(url, 'path')
        self.sendReplyImage(matId, to, path)
        return self.deleteFile(path)

    @loggedIn
    def sendMentionV2(self, id, to, text="", mids=[], isUnicode=False):
        arrData = ""
        arr = []
        mention = "@zeroxyuuki "
        if mids == []:
            raise Exception("Invalid mids")
        if "@!" in text:
            if text.count("@!") != len(mids):
                raise Exception("Invalid mids")
            texts = text.split("@!")
            textx = ""
            unicode = ""
            if isUnicode:
                for mid in mids:
                    unicode += str(texts[mids.index(mid)].encode('unicode-escape'))
                    textx += str(texts[mids.index(mid)])
                    slen = len(textx) if unicode == textx else len(textx) + unicode.count('U0')
                    elen = len(textx) + 15
                    arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
                    arr.append(arrData)
                    textx += mention
            else:
                for mid in mids:
                    textx += str(texts[mids.index(mid)])
                    slen = len(textx)
                    elen = len(textx) + 15
                    arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
                    arr.append(arrData)
                    textx += mention
            textx += str(texts[len(mids)])
        else:
            raise Exception("Invalid mention position")
        self.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0, msgid=id)

    @loggedIn
    def sendMessageaaaa(self, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)
    def sendMessage(self, to, text, contentMetadata={}, contentType=0,msgid=None):
        #msg = self.generateReplyMessage(relatedMessageId)
        msg = Message()
        if 'MENTION' in contentMetadata.keys()!=None:
            try:
                msg.relatedMessageId = str(self.talk.getRecentMessagesV2(to, 10)[0].id)
                msg.relatedMessageServiceCode = 1
                msg.messageRelationType = 3
            except:
                pass
        if msgid != None:
            msg.relatedMessageId = str(msgid)
            msg.relatedMessageServiceCode = 1
            msg.messageRelationType = 3
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)
    """ Usage:
        @to Integer
        @text String
        @dataMid List of user Mid
    """
    @loggedIn
    def sendMessages(self, messageObject):
        return self.talk.sendMessage(0, messageObject)

    def giftmessage(self,to):
        a = ("5","7","6","8")
        b = random.choice(a)
        return self.sendMessage(to, text=None, contentMetadata={'PRDTYPE': 'STICKER','STKVER': '1','MSGTPL': b,'STKPKGID': '1380280'}, contentType=9)
    
    def adityarequestweb(self,url):
        r = requests.get("{}".format(url))
        data = r.text
        data = json.loads(data)
        return data
    
    def templatefoot(self,link,AI,AN):
        a={'AGENT_LINK': link,
        'AGENT_ICON': AI,
        'AGENT_NAME': AN}
        return a
    
    def blekedok(self,t:int=None,tt:str=None):
        r = requests.get('https://www.webtoons.com/id/genre')
        soup = BeautifulSoup(r.text,'html5lib')
        data = soup.find_all(class_='card_lst')
        datea = data[t].find_all(class_='info')
        if tt == 'data':
            return datea
        else:
            return data[t].find_all('a')
    
    def restart_program(self):
        os.system('clear')
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def getalbum(self, to, wait):
        ha = self.getGroupAlbum(to)
        a = [a['title'] for a in ha['result']['items']];c=[a['photoCount'] for a in ha['result']['items']]
        b = '╭「 Album Group 」'
        no=0
        for i in range(len(a)):
            no+=1
            if no == len(a):b+= '\n╰{}. {} | {}'.format(no,a[i],c[i])
            else:b+= '\n│{}. {} | {}'.format(no,a[i],c[i])
        self.sendMessage(to,"{}".format(b))
    
    def debug(self):
        get_profile_time_start = time.time()
        get_profile = self.getProfile()
        get_profile_time = time.time() - get_profile_time_start
        get_group_time_start = time.time()
        get_group = self.getGroupIdsJoined()
        get_group_time = time.time() - get_group_time_start
        get_contact_time_start = time.time()
        get_contact = self.getContact(get_profile.mid)
        get_contact_time = time.time() - get_contact_time_start
        return " 「 Debug 」\nType:\n - Get Profile\n   %.10f\n - Get Contact\n   %.10f\n - Get Group\n   %.10f" % (get_profile_time/2,get_contact_time/2,get_group_time/2)

    def getinformations(self,to,mid,wait):
        try:
            if mid in wait["whitelist"]:a = "Whitelisted: Yes"
            else:a = "Whitelisted: No"
            if mid in wait["blacklist"]:b = "Blacklisted: Yes"
            else:b = "Blacklisted: No"
            h = self.getContact(mid).statusMessage
            if h == '':hh = '\n'
            else:hh = "Status:\n" + h + "\n\n"
            zxc = " 「 ID 」\nName: @!\n" + hh + "User ID:\n" + mid + "\n"+a+" "+b
            self.sendMention(to, zxc, '',[mid])
            self.sendContact(to,mid)
        except:
            ginfo = self.getCompactGroup(mid)
            try:
                gCreators = ginfo.creator.mid;gtime = ginfo.createdTime
            except:
                gCreators = ginfo.members[0].mid;gtime = ginfo.createdTime
            if ginfo.invitee is None:
                sinvitee = "0"
            else:
                sinvitee = str(len(ginfo.invitee))
            if ginfo.preventedJoinByTicket == True:u = "Disable"
            else:u = "line://ti/g/" + self.reissueGroupTicket(mid)
            zxc = " 「 ID 」\nGroup Name:\n{}\n\nGroup ID:\n{}\n\nAnggota: {}\nInvitation: {}\nTicket:{}\n\nCreated at:\n{}\nby @!".format(ginfo.name,mid,len(ginfo.members),sinvitee,u,humanize.naturaltime(datetime.fromtimestamp(gtime/1000)))
            self.sendMention(to,zxc,'',[gCreators])
            self.sendContact(to,gCreators)
    def getinformation(self,to,mid,wait):
        try:
            if mid in wait["whitelist"]:a = "Whitelisted: Yes"
            else:a = "Whitelisted: No"
            if mid in wait["blacklist"]:b = "Blacklisted: Yes"
            else:b = "Blacklisted: No"
            h = self.getContact(mid).statusMessage
            if h == '':hh = '\n'
            else:hh = "Status:\n" + h + "\n\n"
            zxc = " 「 ID 」\nName: @!\n" + hh + "User ID:\n" + mid + "\n"+a+" "+b
            self.sendMention(to, zxc, '',[mid])
            self.sendContact(to,mid)
        except:
            ginfo = self.getCompactGroup(mid)
            try:
                gCreators = ginfo.creator.mid;gtime = ginfo.createdTime
            except:
                gCreators = ginfo.members[0].mid;gtime = ginfo.createdTime
            if ginfo.invitee is None:
                sinvitee = "0"
            else:
                sinvitee = str(len(ginfo.invitee))
            if ginfo.preventedJoinByTicket == True:u = "Disable"
            else:u = "line://ti/g/" + self.reissueGroupTicket(mid)
            zxc = " 「 ID 」\nGroup Name:\n{}\n\nGroup ID:\n{}\n\nAnggota: {}\nInvitation: {}\nTicket:{}\n\nCreated at:\n{}\nby @!".format(ginfo.name,mid,len(ginfo.members),sinvitee,u,humanize.naturaltime(datetime.fromtimestamp(gtime/1000)))
            self.sendMention(to,zxc,'',[gCreators])
            self.sendContact(to,gCreators)
    
    def sendMention(self,to, text="",ps='', mids=[]):
        arrData = ""
        arr = []
        mention = "@RhyN It's me "
        if mids == []:
            raise Exception("Invalid mids")
        if "@!" in text:
            if text.count("@!") != len(mids):
                raise Exception("Invalid mids")
            texts = text.split("@!")
            textx = ''
            h = ''
            for mid in range(len(mids)):
                h+= str(texts[mid].encode('unicode-escape'))
                textx += str(texts[mid])
                if h != textx:slen = len(textx)+h.count('U0');elen = len(textx)+h.count('U0') + 13
                else:slen = len(textx);elen = len(textx) + 13
                arrData = {'S':str(slen), 'E':str(elen), 'M':mids[mid]}
                arr.append(arrData)
                textx += mention
            textx += str(texts[len(mids)])
        else:
            textx = ''
            slen = len(textx)
            elen = len(textx) + 18
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
            arr.append(arrData)
            textx += mention + str(text)
        try:
            try:
                if 'kolori' in ps:contact = self.getContact(ps.split('##')[1])
                else:contact = self.getContact(to)
                cu = "http://profile.line-cdn.net/" + contact.pictureStatus
                cc = str(contact.displayName)
            except Exception as e:
                cdb = self.getContact(self.profile.mid)
                cc = str(cdb.displayName)
                cu = "http://profile.line-cdn.net/" + cdb.pictureStatus
            self.sendMessage(to, textx, {'AGENT_LINK': "line://app/1602687308-DgedGk9A?type=fotext&text=I'm%20RhyN",'AGENT_ICON': "http://dl.profile.line-cdn.net/" + self.getProfile().picturePath,'AGENT_NAME':ps,'MSG_SENDER_ICON':cu,'MSG_SENDER_NAME':cc,'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')},0)
        except:
            try:
                self.sendMessage(to, textx, {'AGENT_LINK': "line://app/1602687308-DgedGk9A?type=fotext&text=I'm%20RhyN",'AGENT_ICON': "http://dl.profile.line-cdn.net/" + self.getProfile().picturePath,'MSG_SENDER_NAME': self.getContact(to).displayName,'MSG_SENDER_ICON': 'http://dl.profile.line-cdn.net/' + self.getContact(to).pictureStatus,'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')},0)
            except:
                try:
                    self.sendMessage(to, textx, {'AGENT_LINK': "line://app/1602687308-DgedGk9A?type=fotext&text=I'm%20RhyN",'AGENT_ICON': "http://dl.profile.line-cdn.net/" + self.getProfile().picturePath,'MSG_SENDER_NAME': self.getContact("u085311ecd9e3e3d74ae4c9f5437cbcb5").displayName,'MSG_SENDER_ICON': 'http://dl.profile.line-cdn.net/' + self.getContact("u085311ecd9e3e3d74ae4c9f5437cbcb5").pictureStatus,'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                except:
                    self.sendMessage(to, textx, {'AGENT_LINK': "line://app/1602687308-DgedGk9A?type=fotext&text=I'm%20RhyN",'AGENT_ICON': "http://dl.profile.line-cdn.net/" + self.getProfile().picturePath,'AGENT_NAME':ps,'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')},0)
    
    def sendMention2(self,to, text="",ps='', mids=[]):
        arrData = ""
        arr = []
        mention = "@MentionOrang "
        if mids == []:
            raise Exception("Invalid mids")
        if "@!" in text:
            if text.count("@!") != len(mids):
                raise Exception("Invalid mids")
            texts = text.split("@!")
            textx = ''
            h = ''
            for mid in range(len(mids)):
                h+= str(texts[mid].encode('unicode-escape'))
                textx += str(texts[mid])
                if h != textx:slen = len(textx)+h.count('U0');elen = len(textx)+h.count('U0') + 13
                else:slen = len(textx);elen = len(textx) + 13
                arrData = {'S':str(slen), 'E':str(elen), 'M':mids[mid]}
                arr.append(arrData)
                textx += mention
            textx += str(texts[len(mids)])
        else:
            textx = ''
            slen = len(textx)
            elen = len(textx) + 18
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
            arr.append(arrData)
            textx += mention + str(text)
        self.sendMessage(to, textx, {'AGENT_LINK': 'line://ti/p/~{}'.format(self.profile.userid),'AGENT_ICON': "http://dl.profile.line-cdn.net/" + self.getProfile().picturePath,'AGENT_NAME': ps,'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    
    def image_search(self, query):
        query = query.replace(' ', "%20")
        url = "https://www.google.com/search?hl=en&site=imghp&tbm=isch&tbs=isz:l&q=" + query
        mozhdr = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"}
        req = requests.get(url, headers = mozhdr)
        soupeddata = BeautifulSoup(req.content , "lxml")
        images = soupeddata.find_all("div", {"class": "rg_meta notranslate"})
        aa = random.randint(0,len(images))
        try:
            images = json.loads(images[aa].text)
            return images
        except Exception as e:return e
    
    def forward(self,msg,kuciyose):
        if msg.toType == 2:msg.to = msg.to
        else:msg.to = msg._from
        if msg.contentType == 1:
            try:
                if msg.contentMetadata != {}:
                    path = self.downloadObjectMsg(msg.id,'path','dataSeen/m.gif',True)
                    a = threading.Thread(target=self.sendGIF, args=(msg.to,path,)).start()
            except:self.sendImageWithURL(msg.to,'https://obs-sg.line-apps.com/talk/m/download.nhn?oid='+msg.id)
        if msg.contentType == 2:self.sendVideoWithURL(msg.to,'https://obs-sg.line-apps.com/talk/m/download.nhn?oid='+msg.id)
        if msg.contentType == 3:self.sendAudioWithURL(msg.to,'https://obs-sg.line-apps.com/talk/m/download.nhn?oid='+msg.id)
    
    def limitlimit(self,to,wait):
        try:
            if to in wait['talkblacklist']['tos']:
                if wait['talkblacklist']['tos'][to]["expire"] == True:
                    return
                elif time.time() - wait['talkblacklist']['tos'][to]["time"] <= 5:
                    wait['talkblacklist']['tos'][to]["flood"] += 1
                    if wait['talkblacklist']['tos'][to]["flood"] >= 15:
                        wait['talkblacklist']['tos'][to]["flood"] = 0
                        wait['talkblacklist']['tos'][to]["expire"] = True
                        self.sendMessage(to, " 「 FLOOD 」\nFLOOD DETECT, I will mute on 30second in this room")
                else:
                    wait['talkblacklist']['tos'][to]["flood"] = 0
                    wait['talkblacklist']['tos'][to]["time"] = time.time()
            else:
                wait['talkblacklist']['tos'][to] = {"time": time.time(),"flood": 0,"expire": False}
        except:wait['talkblacklist']['tos'] = {}
    
    def templatefoot(self,link,AI,AN):
        a={'AGENT_LINK': link,
        'AGENT_ICON': AI,
        'AGENT_NAME': AN}
        return a

    def waktunjir(self):
        sd = ''
        if datetime.now().hour > 1 and datetime.now().hour <10:sd+= 'Good Morning'
        if datetime.now().hour > 10 and datetime.now().hour <15:sd+= 'Good Afternoon'
        if datetime.now().hour > 15 and datetime.now().hour <18:sd+= 'Good Evening'
        if datetime.now().hour >= 18:sd+= 'Good Night'
        return sd
    
    def adityasplittext(self,text,lp=''):
        separate = text.split(" ")
        if lp == '':adalah = text.replace(separate[0]+" ","")
        elif lp == 's':adalah = text.replace(separate[0]+" "+separate[1]+" ","")
        else:adalah = text.replace(separate[0]+" "+separate[1]+" "+separate[2]+" ","")
        return adalah
    
    def mycmd(self,text,wait):
        cmd = ''
        pesan = text.lower()
        if wait['setkey'] != '':
            if pesan.startswith(wait['setkey']):
                cmd = pesan.replace(wait['setkey']+' ','').replace(wait['setkey'],'')
        else:
            cmd = text
        return cmd
    
    @loggedIn
    def sendSticker(self, to, packageId, stickerId):
        contentMetadata = {
            'STKVER': '100',
            'STKPKGID': packageId,
            'STKID': stickerId
        }
        return self.sendMessage(to, '', contentMetadata, 7)
        
    @loggedIn
    def sendContact(self, to, mid):
        contentMetadata = {'mid': mid}
        return self.sendMessage(to, '', contentMetadata, 13)

    @loggedIn
    def sendGift(self, to, productId, productType):
        if productType not in ['theme','sticker']:
            raise Exception('Invalid productType value')
        contentMetadata = {
            'MSGTPL': str(randint(0, 12)),
            'PRDTYPE': productType.upper(),
            'STKPKGID' if productType == 'sticker' else 'PRDID': productId
        }
        return self.sendMessage(to, '', contentMetadata, 9)

    @loggedIn
    def sendMessageAwaitCommit(self, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessageAwaitCommit(self._messageReq[to], msg)

    @loggedIn
    def unsendMessage(self, messageId):
        self._unsendMessageReq += 1
        return self.talk.unsendMessage(self._unsendMessageReq, messageId)

    @loggedIn
    def requestResendMessage(self, senderMid, messageId):
        return self.talk.requestResendMessage(0, senderMid, messageId)

    @loggedIn
    def respondResendMessage(self, receiverMid, originalMessageId, resendMessage, errorCode):
        return self.talk.respondResendMessage(0, receiverMid, originalMessageId, resendMessage, errorCode)

    @loggedIn
    def removeMessage(self, messageId):
        return self.talk.removeMessage(messageId)
    
    @loggedIn
    def removeAllMessages(self, lastMessageId):
        return self.talk.removeAllMessages(0, lastMessageId)

    @loggedIn
    def removeMessageFromMyHome(self, messageId):
        return self.talk.removeMessageFromMyHome(messageId)
    
    @loggedIn
    def sendChatChecked(self, consumer, messageId):
        return self.talk.sendChatChecked(0, consumer, messageId)

    @loggedIn
    def sendEvent(self, messageObject):
        return self.talk.sendEvent(0, messageObject)

    @loggedIn
    def getLastReadMessageIds(self, chatId):
        return self.talk.getLastReadMessageIds(0, chatId)

    @loggedIn
    def getPreviousMessagesV2WithReadCount(self, messageBoxId, endMessageId, messagesCount=50):
        return self.talk.getPreviousMessagesV2WithReadCount(messageBoxId, endMessageId, messagesCount)

    """Object"""

    @loggedIn
    def sendImage(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentType = 1).id
        return self.uploadObjTalk(path=path, type='image', returnAs='bool', objId=objectId)
    
    def sendImage2(self, to, path,texk='Image'):
        objectId = self.sendMessage(to=to, text=None,contentMetadata={'AGENT_ICON': "http://dl.profile.line-cdn.net/" + self.getProfile().picturePath, 'AGENT_NAME': texk, 'AGENT_LINK': 'line://ti/p/~{}'.format(self.getProfile().userid)}, contentType = 1).id
        return self.uploadObjTalk(path=path, type='image', returnAs='bool', objId=objectId)
    
    @loggedIn
    def sendImages(self, to, path,texk='Image',tt=''):
        asda = True
        kui = 0
        while asda:
            if kui >= 40:
                asda = False
            else:
                try:
                    objectId = self.sendMessage(to=to, text=None,contentMetadata={'MSG_SENDER_ICON':texk,'MSG_SENDER_NAME':tt}, contentType = 1).id
                    self.uploadObjTalk(path=path, type='image', returnAs='bool', objId=objectId)
                    asda = False
                except Exception as e:
                    kui += 1
    def sendImage5(self, to, path,texk='Image',tt=''):
        asda = True
        kui = 0
        while asda:
            if kui >= 5:
                asda = False
            else:
                try:
                    objectId = self.sendMessage(to=to, text=None, contentType = 1,msgid=tt).id
                    self.uploadObjTalk(path=path, type='image', returnAs='bool', objId=objectId)
                    asda = False
                except Exception as e:
                    kui += 1
    def sendImagenih(self, to, path,texk='Image',tt=''):
        asda = True
        kui = 0
        while asda:
            if kui >= 5:
                asda = False
            else:
                try:
                    objectId = self.sendMessage(to=to, text=None, contentType = 1,msgid=tt).id
                    self.uploadObjTalk(path=path, type='image', returnAs='bool', objId=objectId)
                    asda = False
                except Exception as e:
                    kui += 1
    def sendImageWithURL5(self, to, url,texk='Image',tt=''):
        path = self.downloadFileURL(url, 'path')
        self.sendImage5(to, path,texk,tt)
        return os.remove(path)
    def sendImageWithURLs(self, to, url,texk='Image',tt=''):
        path = self.downloadFileURL(url, 'path')
        self.sendImages(to, path,texk,tt)
        return os.remove(path)
    def sendImageWithurl(self, to, url,texk='Image',tt=''):
        path = self.downloadFileURL(url, 'path')
        self.sendImagenih(to, path,texk,tt)
        return os.remove(path)
    def sendImageWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendImage(to, path)
    def sendVideoWithurl(self, to, url,msgid=''):
        path = self.downloadFileURL(url, 'path')
        return self.sendVideos(to, path,msgid=msgid)
    def sendImageWithURL2(self, to, url,texk='Image'):
        path = self.downloadFileURL(url, 'path')
        return self.sendImage2(to, path,texk)
    def sendVideos(self, to, path,t='60000',msgid=''):
        objectId = self.sendMessage(to=to, text=None, contentMetadata={'VIDLEN': t,'DURATION': t}, contentType = 2,msgid=msgid).id
        return self.uploadObjTalk(path=path, type='video', returnAs='bool', objId=objectId)
        os.remove(path)
    @loggedIn
    def sendGIF(self, to, path):
        return self.uploadObjTalk(path=path, type='gif', returnAs='bool', to=to)

    @loggedIn
    def sendGIFWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendGIF(to, path)

    @loggedIn
    def sendVideo(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentMetadata={'VIDLEN': '60000','DURATION': '60000'}, contentType = 2).id
        return self.uploadObjTalk(path=path, type='video', returnAs='bool', objId=objectId)

    @loggedIn
    def sendVideoWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendVideo(to, path)

    @loggedIn
    def sendAudio(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentType = 3).id
        return self.uploadObjTalk(path=path, type='audio', returnAs='bool', objId=objectId)

    @loggedIn
    def sendAudioWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendAudio(to, path)

    @loggedIn
    def sendFile(self, to, path, file_name=''):
        if file_name == '':
            file_name = ntpath.basename(path)
        file_size = len(open(path, 'rb').read())
        objectId = self.sendMessage(to=to, text=None, contentMetadata={'FILE_NAME': str(file_name),'FILE_SIZE': str(file_size)}, contentType = 14).id
        return self.uploadObjTalk(path=path, type='file', returnAs='bool', objId=objectId)

    @loggedIn
    def sendFileWithURL(self, to, url, fileName=''):
        path = self.downloadFileURL(url, 'path')
        return self.sendFile(to, path, fileName)

    """Contact"""
        
    @loggedIn
    def blockContact(self, mid):
        return self.talk.blockContact(0, mid)

    @loggedIn
    def unblockContact(self, mid):
        return self.talk.unblockContact(0, mid)

    @loggedIn
    def findAndAddContactByMetaTag(self, userid, reference):
        return self.talk.findAndAddContactByMetaTag(0, userid, reference)

    @loggedIn
    def findAndAddContactsByMid(self, mid):
        return self.talk.findAndAddContactsByMid(0, mid, 0, '')

    @loggedIn
    def findAndAddContactsByEmail(self, emails=[]):
        return self.talk.findAndAddContactsByEmail(0, emails)

    @loggedIn
    def findAndAddContactsByUserid(self, userid):
        return self.talk.findAndAddContactsByUserid(0, userid)

    @loggedIn
    def findContactsByUserid(self, userid):
        return self.talk.findContactByUserid(userid)

    @loggedIn
    def findContactByTicket(self, ticketId):
        return self.talk.findContactByUserTicket(ticketId)

    @loggedIn
    def getAllContactIds(self):
        return self.talk.getAllContactIds()

    @loggedIn
    def getBlockedContactIds(self):
        return self.talk.getBlockedContactIds()

    @loggedIn
    def getContact(self, mid):
        return self.talk.getContact(mid)

    @loggedIn
    def getContacts(self, midlist):
        return self.talk.getContacts(midlist)

    @loggedIn
    def getFavoriteMids(self):
        return self.talk.getFavoriteMids()

    @loggedIn
    def getHiddenContactMids(self):
        return self.talk.getHiddenContactMids()

    @loggedIn
    def tryFriendRequest(self, midOrEMid, friendRequestParams, method=1):
        return self.talk.tryFriendRequest(midOrEMid, method, friendRequestParams)

    @loggedIn
    def makeUserAddMyselfAsContact(self, contactOwnerMid):
        return self.talk.makeUserAddMyselfAsContact(contactOwnerMid)

    @loggedIn
    def getContactWithFriendRequestStatus(self, id):
        return self.talk.getContactWithFriendRequestStatus(id)

    @loggedIn
    def reissueUserTicket(self, expirationTime=100, maxUseCount=100):
        return self.talk.reissueUserTicket(expirationTime, maxUseCount)
    
    def deleteContact(self,contact):
        try:
            self.talk.updateContactSetting(0,contact,ContactSetting.CONTACT_SETTING_DELETE,'True')
        except:
            traceback.print_exc()
        pass
    
    def clearContacts(self):
        t = self.getContacts(self.getAllContactIds())
        for n in t:
            try:
                self.deleteContact(n.mid)
            except:
                pass
        pass
    def refreshContacts(self):
        contact_ids = self.getAllContactIds()
        contacts    = self.getContacts(contact_ids)
        
        contacts = [contact.displayName+',./;'+contact.mid for contact in contacts]
        contacts.sort()
        contacts = [a.split(',./;')[1] for a in contacts]
        return contacts
    
    @loggedIn
    def cloneContactProfile(self, mid):
        contact = self.getContact(mid)
        profile = self.profile
        profile.displayName = contact.displayName
        profile.statusMessage = contact.statusMessage
        profile.pictureStatus = self.downloadFileURL('http://dl.profile.line-cdn.net/' + contact.pictureStatus, 'path')
        if self.getProfileCoverId(mid) is not None:
            self.updateProfileCoverById(self.getProfileCoverId(mid))
        if profile.videoProfile is None:
            self.updateProfilePicture(profile.pictureStatus)
        return self.updateProfile(profile)

    """Group"""
    @loggedIn
    def getChatRoomAnnouncementsBulk(self, chatRoomMids):
        return self.talk.getChatRoomAnnouncementsBulk(chatRoomMids)

    @loggedIn
    def getChatRoomAnnouncements(self, chatRoomMid):
        return self.talk.getChatRoomAnnouncements(chatRoomMid)

    @loggedIn
    def createChatRoomAnnouncement(self, chatRoomMid, type, contents):
        return self.talk.createChatRoomAnnouncement(0, chatRoomMid, type, contents)
    
    def getannoun(self,to,wait,text):
        text = text.lower()
        a = self.getChatRoomAnnouncements(to)
        if a == []:
            self.sendMention(to, 'Sorry @!In {} nothink get a Announcements'.format(self.getGroup(to).name),' 「 Announcements 」\n', [self.getProfile().mid])
            return
        c = ' 「 Announcements 」'
        no = 0
        h = []
        ds = [a[b].creatorMid for b in range(len(a)) if a[b].creatorMid not in h]
        if text.lower() == 'get announ':
            for b in a:
                if b.creatorMid not in h:
                    h.append(b.creatorMid)
                    no += 1
                    c += "\n{}. @! #{}x".format(no,str(a).count(b.creatorMid))
            self.sendMention(to,c,'',h)
        if text.lower().startswith("get announ "):
            if len(text.split(' ')) == 3:
                sd = ds[int(text.split(' ')[2])-1]
                c+= '\nCreate by: @!'
                no=0
                for b in a:
                    if b.contents.link != None:
                        if b.creatorMid in sd:
                            no+=1
                            if 'line://nv/chatMsg?chatId=' in b.contents.link:sdg = '{}'.format(b.contents.link)
                            else:sdg = '{}'.format(b.contents.text)
                            if no == 1:c+= '\n{}. 「 {} 」\n{}'.format(no,humanize.naturaltime(datetime.fromtimestamp(b.createdTime/1000)),sdg)
                            else:c+= '\n\n{}. 「 {} 」\n{}'.format(no,humanize.naturaltime(datetime.fromtimestamp(b.createdTime/1000)),sdg)
                self.sendMention(to,c,'',[sd])
    
    @loggedIn
    def removeChatRoomAnnouncement(self, chatRoomMid, announcementSeq):
        return self.talk.removeChatRoomAnnouncement(0, chatRoomMid, announcementSeq)

    @loggedIn
    def getGroupWithoutMembers(self, groupId):
        return self.talk.getGroupWithoutMembers(groupId)
    
    @loggedIn
    def findGroupByTicket(self, ticketId):
        return self.talk.findGroupByTicket(ticketId)

    @loggedIn
    def acceptGroupInvitation(self, groupId):
        return self.talk.acceptGroupInvitation(0, groupId)

    @loggedIn
    def acceptGroupInvitationByTicket(self, groupId, ticketId):
        return self.talk.acceptGroupInvitationByTicket(0, groupId, ticketId)

    @loggedIn
    def cancelGroupInvitation(self, groupId, contactIds):
        return self.talk.cancelGroupInvitation(0, groupId, contactIds)

    @loggedIn
    def createGroup(self, name, midlist):
        return self.talk.createGroup(0, name, midlist)

    @loggedIn
    def getGroup(self, groupId):
        return self.talk.getGroup(groupId)

    @loggedIn
    def getGroups(self, groupIds):
        return self.talk.getGroups(groupIds)

    @loggedIn
    def getGroupsV2(self, groupIds):
        return self.talk.getGroupsV2(groupIds)

    @loggedIn
    def getCompactGroup(self, groupId):
        return self.talk.getCompactGroup(groupId)

    @loggedIn
    def getCompactRoom(self, roomId):
        return self.talk.getCompactRoom(roomId)

    @loggedIn
    def getGroupIdsByName(self, groupName):
        gIds = []
        for gId in self.getGroupIdsJoined():
            g = self.getCompactGroup(gId)
            if groupName in g.name:
                gIds.append(gId)
        return gIds

    @loggedIn
    def getGroupIdsInvited(self):
        return self.talk.getGroupIdsInvited()

    @loggedIn
    def getGroupIdsJoined(self):
        return self.talk.getGroupIdsJoined()

    @loggedIn
    def updateGroupPreferenceAttribute(self, groupMid, updatedAttrs):
        return self.talk.updateGroupPreferenceAttribute(0, groupMid, updatedAttrs)

    @loggedIn
    def inviteIntoGroup(self, groupId, midlist):
        return self.talk.inviteIntoGroup(0, groupId, midlist)

    @loggedIn
    def kickoutFromGroup(self, groupId, midlist):
        return self.talk.kickoutFromGroup(0, groupId, midlist)

    @loggedIn
    def leaveGroup(self, groupId):
        return self.talk.leaveGroup(0, groupId)

    @loggedIn
    def rejectGroupInvitation(self, groupId):
        return self.talk.rejectGroupInvitation(0, groupId)

    @loggedIn
    def reissueGroupTicket(self, groupId):
        return self.talk.reissueGroupTicket(groupId)

    @loggedIn
    def updateGroup(self, groupObject):
        return self.talk.updateGroup(0, groupObject)

    """Room"""

    @loggedIn
    def createRoom(self, midlist):
        return self.talk.createRoom(0, midlist)

    @loggedIn
    def getRoom(self, roomId):
        return self.talk.getRoom(roomId)

    @loggedIn
    def inviteIntoRoom(self, roomId, midlist):
        return self.talk.inviteIntoRoom(0, roomId, midlist)

    @loggedIn
    def leaveRoom(self, roomId):
        return self.talk.leaveRoom(0, roomId)

    """Call"""
        
    @loggedIn
    def acquireCallTalkRoute(self, to):
        return self.talk.acquireCallRoute(to)
    
    """Report"""

    @loggedIn
    def reportSpam(self, chatMid, memberMids=[], spammerReasons=[], senderMids=[], spamMessageIds=[], spamMessages=[]):
        return self.talk.reportSpam(chatMid, memberMids, spammerReasons, senderMids, spamMessageIds, spamMessages)
        
    @loggedIn
    def reportSpammer(self, spammerMid, spammerReasons=[], spamMessageIds=[]):
        return self.talk.reportSpammer(spammerMid, spammerReasons, spamMessageIds)
