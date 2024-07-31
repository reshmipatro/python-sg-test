import hashlib
from cryptography.hazmat.primitives import hashes
from Crypto.Hash import MD5 as pycrypto_md5
from Crypto.Hash import SHA3_256 as pycrypto_sha3
from Cryptodome.Hash import MD5
from Cryptodome.Hash import SHA3_256

# ruleid:insecure-hash-functions
hashlib.new('md5')

# ruleid:insecure-hash-functions
hashlib.new('md4', 'test')

# ruleid:insecure-hash-functions
hashlib.new(name='md5', string='test')

# ruleid:insecure-hash-functions
hashlib.new('MD4', string='test')

# ruleid:insecure-hash-functions
hashlib.new(string='test', name='MD5')

# ruleid:insecure-hash-functions
hashlib.sha1()

# ruleid:insecure-hash-functions
hashlib.new('sha1')

# ruleid:insecure-hash-functions
hashlib.new(string='test', name='SHA1')

# ok:insecure-hash-functions
hashlib.new('SHA512')

# ok:insecure-hash-functions
hashlib.new(string='test', name='SHA3')

# ok:insecure-hash-functions
hashlib.new('sha256')

# ruleid:insecure-hash-functions
hashes.MD5()
# ok:insecure-hash-functions
hashes.SHA256()
# ok:insecure-hash-functions
hashes.SHA3_256()

# ruleid:insecure-hash-functions
hash = pycrypto_md5.new()
# ok:insecure-hash-functions
hash = pycrypto_sha3.new()

# ruleid:insecure-hash-functions
hash = MD5.new()
# ok:insecure-hash-functions
hash = SHA3_256.new()
