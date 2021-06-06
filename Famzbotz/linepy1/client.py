# -*- coding: utf-8 -*-
from akad.ttypes import Message
from .auth import Auth
from .models import Models
from .talk import Talk
from .square import Square
from .call import Call
from .timeline import Timeline
from .shop import Shop

class LINE(Auth, Models, Talk, Square, Call, Timeline, Shop):

    def __init__(self, idOrAuthToken=None, passwd=None, certificate=None, systemName=None, appName=None, showQr=False, keepLoggedIn=True, _to=None, _client=None):
        
        Auth.__init__(self)
        if not (idOrAuthToken or idOrAuthToken and passwd):
            if _to is None and _client is None:
                self.loginWithQrCode(keepLoggedIn=keepLoggedIn, systemName=systemName, appName=appName, showQr=showQr)
            else:
                self.loginWithQrCode(keepLoggedIn=keepLoggedIn, systemName=systemName, appName=appName, showQr=showQr, _to = _to, _client=_client)
        if idOrAuthToken and passwd:
            self.loginWithCredential(_id=idOrAuthToken, passwd=passwd, certificate=certificate, systemName=systemName, appName=appName, keepLoggedIn=keepLoggedIn)
        elif idOrAuthToken and not passwd:
            #if _to is None and _client is None:
            self.loginWithAuthToken(authToken=idOrAuthToken, appName=appName)
            #else:
            #    self.loginWithAuthToken(authToken=idOrAuthToken, appName=appName, _to=_to, _client=_client)
        self.__initAll()

    def __initAll(self):

        self.profile    = self.talk.getProfile()
        self.groups     = self.talk.getGroupIdsJoined()

        Models.__init__(self)
        Talk.__init__(self)
        #Square.__init__(self)
        Call.__init__(self)
        Timeline.__init__(self)
        Shop.__init__(self)
