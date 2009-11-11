from twisted.application.service import ServiceMaker

XMLRPCIM = ServiceMaker(
    "xmlrpcim",
    "nous.im.tap",
    "XMLRPC IM service",
    "nous.im"
)
