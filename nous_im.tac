# -*- mode: python -*-
import os
from twisted.application import service, internet
from twisted.web import server

def getXMLRPCService(gg_factory):
    from nous.im.server import TwistedRPCServer
    s = TwistedRPCServer('user','pass', gg_factory)
    return internet.TCPServer(6001, server.Site(s))

def getIMService():
    from nous.im.gg import GaduTest
    from twistedgadu import GGClientFactory
    t = GaduTest()
    factory = GGClientFactory(t)
    return internet.TCPClient('91.197.13.83', 8074, factory), factory


# this is the core part of any tac file, the creation of the root-level
# application object
application = service.Application("Demo application")

gg_service, gg_factory = getIMService()
gg_service.setServiceParent(application)

# attach the service to its parent application
service = getXMLRPCService(gg_factory)
service.setServiceParent(application)
