from ftplib import FTP, FTP_TLS
import ssl
import pysftp
HOST = "random.ftp.server"
USERNAME = "user"
PASSWORD = "pass"

ftpSession = FTP(HOST)
# ruleid: 319-ftplib
ftpSession.login()

client = FTP(timeout=TIMEOUT, encoding=encoding)
# ruleid: 319-ftplib
client.connect(HOST)

ftpSession2 = FTP_TLS(HOST, USERNAME, PASSWORD, context=ssl.create_default_context())
# ok: 319-ftplib
ftpSession2.login()

# ok: 319-ftplib
pysftp.Connection(HOST, USERNAME, password=PASSWORD)