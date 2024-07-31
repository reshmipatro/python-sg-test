import ssl
from OpenSSL import SSL

#######
# ruleid:327-ssl-tls-version
ssl.wrap_socket(ssl_version=ssl.PROTOCOL_SSLv2)
# ruleid:327-ssl-tls-version
SSL.Context(method=SSL.SSLv23_METHOD)

# ok:327-ssl-tls-version
ssl.wrap_socket(ssl_version=ssl.PROTOCOL_TLSv1_2)

# ruleid:327-ssl-tls-version
some_other_method(ssl_version=ssl.PROTOCOL_SSLv2)
# ruleid:327-ssl-tls-version
some_other_method(method=SSL.SSLv2_METHOD)
# ruleid:327-ssl-tls-version
some_other_method(method=SSL.SSLv23_METHOD)

# ruleid:327-ssl-tls-version
ssl.wrap_socket(ssl_version=ssl.PROTOCOL_SSLv3)
# ruleid:327-ssl-tls-version
ssl.wrap_socket(ssl_version=ssl.PROTOCOL_TLSv1)
# ruleid:327-ssl-tls-version
SSL.Context(method=SSL.SSLv3_METHOD)
# ruleid:327-ssl-tls-version
SSL.Context(method=SSL.TLSv1_METHOD)

# ruleid:327-ssl-tls-version
some_other_method(ssl_version=ssl.PROTOCOL_SSLv3)
# ruleid:327-ssl-tls-version
some_other_method(ssl_version=ssl.PROTOCOL_TLSv1)
# ruleid:327-ssl-tls-version
some_other_method(method=SSL.SSLv3_METHOD)
# ruleid:327-ssl-tls-version
some_other_method(method=SSL.TLSv1_METHOD)

#######

# ruleid: 327-ssl-tls-version
ssl.wrap_socket(ssl_version=ssl.PROTOCOL_TLSv1_1)

# ruleid: 327-ssl-tls-version
SSL.Context(method=SSL.TLSv1_1_METHOD)

# ruleid: 327-ssl-tls-version
ssl.wrap_socket(ssl_version=ssl.PROTOCOL_SSLv2)
# ruleid: 327-ssl-tls-version
SSL.Context(method=SSL.SSLv2_METHOD)
# ruleid: 327-ssl-tls-version
SSL.Context(method=SSL.SSLv23_METHOD)
# ruleid: 327-ssl-tls-version
ssl.wrap_socket(ssl_version=ssl.PROTOCOL_SSLv3)
# ruleid: 327-ssl-tls-version
SSL.Context(method=SSL.SSLv3_METHOD)

# ruleid: 327-ssl-tls-version
ssl.wrap_socket(ssl_version=ssl.PROTOCOL_TLSv1)
# ruleid: 327-ssl-tls-version
SSL.Context(method=SSL.TLSv1_METHOD)
# ok: 327-ssl-tls-version
SSL.Context(method=SSL.TLS1_3_VERSION)


context = SSL.Context(SSL.TLS_SERVER_METHOD)
# ok: 327-ssl-tls-version
context.set_min_proto_version(SSL.TLS1_3_VERSION)

def fun():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # ok: 327-ssl-tls-version
    context.minimum_version = ssl.TLSVersion.TLSv1_3

def no_fun():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # ruleid: 327-ssl-tls-version
    context.minimum_version = ssl.TLSVersion.TLSv1_1

# These were here before, but I don't think it makes sense to not match them.
# If the ssl/OpenSSL libraries are imported and we detect a bad looking SSL version
# constant, then we should still flag it.
# todook: 327-ssl-tls-version
herp_derp(ssl_version=ssl.PROTOCOL_SSLv3)
# todook: 327-ssl-tls-version
herp_derp(ssl_version=ssl.PROTOCOL_TLSv1)
# todook: 327-ssl-tls-version
herp_derp(method=SSL.SSLv3_METHOD)
