import os.path

from paste.deploy.loadwsgi import ConfigLoader

from twisted.application import service, internet
from twisted.web import server
from twisted.python import usage

from nous.im.server import TwistedRPCServer
from nous.im.gg import GaduEcho
from nous.im.gg import GGClientFactory


def getGGService(config):
    uin = config.getint('gg', 'uin')
    pwd = config.get('gg', 'password')

    if uin is None or pwd is None:
        return None, None

    factory = GGClientFactory(GaduEcho(uin, pwd))
    return internet.TCPClient('91.197.13.83', 8074, factory), factory


def getSkypeService(config):
    return None, None


def getJabberService(config):
    return None, None


def getXMLRPCService(config,
                     gg_factory=None,
                     skype_factory=None,
                     jabber_factory=None):
    username = config.get('xmlrpc', 'username')
    password = config.get('xmlrpc', 'password')
    port = config.get('xmlrpc', 'port')
    s = TwistedRPCServer(username, password, gg_factory)
    return internet.TCPServer(int(port), server.Site(s))


class Options(usage.Options):
    optParameters = [["config", "c", "development.ini", "Configuration file"]]


def makeService(config):
    config_file = os.path.abspath(config['config'])
    parser = ConfigLoader(config_file).parser

    parent_service = service.MultiService()

    gg_factory = None
    if parser.has_section('gg'):
        gg_service, gg_factory = getGGService(parser)
        parent_service.addService(gg_service)

    skype_factory = None
    if parser.has_section('skype'):
        skype_service, skype_factory = getSkypeService(parser)
        parent_service.addService(skype_service)

    jabber_factory = None
    if parser.has_section('jabber'):
        jabber_service, jabber_factory = getJabberService(parser)
        parent_service.addService(jabber_service)

    xml_service = getXMLRPCService(parser,
                                   gg_factory=gg_factory,
                                   skype_factory=skype_factory,
                                   jabber_factory=jabber_factory)
    parent_service.addService(xml_service)
    return parent_service
