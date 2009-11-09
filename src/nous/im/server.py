import xmlrpclib
#from nous.im.gg import getGGCLient
from twisted.web import xmlrpc, server, http
from twisted.internet import defer, reactor

Fault = xmlrpclib.Fault

class TwistedRPCServer(xmlrpc.XMLRPC):
    """ A class which works as an XML-RPC server with
    HTTP basic authentication """

    def __init__(self, user='', password='', ggclient=None):
        self._user = user
        self._password = password
        self._auth = (self._user !='')
        self.ggclient = ggclient
        xmlrpc.XMLRPC.__init__(self)

    def xmlrpc_echo(self, x):
        return x

    def xmlrpc_ping(self):
        return 'OK'

    def xmlrpc_send_gg_msg(self, to, msg):
        self.ggclient.instance.send_msg(to, msg)
        return "OK"

    def render(self, request):
        """ Overridden 'render' method which takes care of
        HTTP basic authorization """

        if self._auth:
            cleartext_token = self._user + ':' + self._password
            user = request.getUser()
            passwd = request.getPassword()

            if user=='' and passwd=='':
                request.setResponseCode(http.UNAUTHORIZED)
                return 'Authorization required!'
            else:
                token = user + ':' + passwd
                if token != cleartext_token:
                    request.setResponseCode(http.UNAUTHORIZED)
                    return 'Authorization Failed!'

        request.content.seek(0, 0)
        args, functionPath = xmlrpclib.loads(request.content.read())
        try:
            function = self._getFunction(functionPath)
        except Fault, f:
            self._cbRender(f, request)
        else:
            request.setHeader("content-type", "text/xml")
            defer.maybeDeferred(function, *args).addErrback(
                self._ebRender
                ).addCallback(
                self._cbRender, request
                )

        return server.NOT_DONE_YET
