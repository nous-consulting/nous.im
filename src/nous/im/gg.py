from twistedgadu import ContactsList
from twisted.internet.protocol import ReconnectingClientFactory
from twistedgadu.main import GGClient
from twistedgadu import GGStatuses


class GaduConnectionManagerBase(object):

    def __init__(self, username, password):
        self.contacts_list = ContactsList()
        self.username, self.password = username, password

    def on_auth_got_seed(self, conn, seed):
        conn.login(seed, self.username, self.password, GGStatuses.Avail, '')

    def on_login_ok(self, conn):
        conn.import_contacts_list()

    def on_login_failed(self, conn):
        pass

    def on_need_email(self, conn):
        pass

    def on_disconnecting(self, conn):
        pass

    def on_notify_reply(self, conn, contacts):
        pass

    def on_msg_recv(self, conn, sender, seq, time, msg_class, message):
        pass

    def on_msg_ack(self, conn, status, recipient, seq):
        pass

    def on_status(self, conn, contact):
        pass

    def on_status60(self, conn, contact):
        pass

    def on_userlist_reply(self, conn, contacts):
        pass

    def on_userlist_exported_or_deleted(self, conn, reqtype, request):
        pass


class GaduEcho(GaduConnectionManagerBase):

    def __init__(self, username, password):
        self.contacts_list = ContactsList()
        self.username, self.password = username, password

    def on_auth_got_seed(self, conn, seed):
        print 'Got seed: ', seed
        conn.login(seed, self.username, self.password, GGStatuses.Avail, '')

    def on_login_ok(self, conn):
        print 'Logged in!'
        super(GaduEcho, self).on_login_ok(conn)

    def on_login_failed(self, conn):
        print 'Failed to log in!'

    def on_need_email(self, conn):
        print 'You must provide an email!'

    def on_disconnecting(self, conn):
        print 'Disconnected!'

    def on_notify_reply(self, conn, contacts):
        print 'Downloaded contact info.'

    def on_msg_recv(self, conn, sender, seq, time, msg_class, message):
        print "Got a message:\nSender: %s\nSeq: %s\n Time: %s\n Class: %s\n Msg: %s\n" % (sender, seq, time, msg_class, message)
        conn.send_msg(sender, message)

    def on_msg_ack(self, conn, status, recipient, seq):
        print "Received confirmation of sending a message:\n   Status: %s\n   Recipient: %s\n   Seq: %s\n" % (status, recipient, seq)

    def on_status(self, conn, contact):
        print "Contact %s changed status to %s, description: %s" % (contact.uin, contact.status, contact.description)

    def on_status60(self, conn, contact):
        print "Contact %s changed status to %s, description: %s" % (contact.uin, contact.status, contact.description)

    def on_userlist_reply(self, conn, contacts):
        print "User list was imported."

    def on_userlist_exported_or_deleted(self, conn, reqtype, request):
        print 'Contact list operation was performed, reqtype - %s, request - %s' % (reqtype, request)


class NousGGClient(GGClient):

    def connectionMade(self):
        GGClient.connectionMade(self)
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)


class GGClientFactory(ReconnectingClientFactory):

    protocol = NousGGClient

    def __init__(self, conn):
        self._conn = conn
        self.clients = []
