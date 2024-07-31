from cryptography.hazmat import backends
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import rsa
from Crypto.PublicKey import DSA as pycrypto_dsa
from Crypto.PublicKey import RSA as pycrypto_rsa
from Crypto.PublicKey import ECC as pycrypto_ecc
from Cryptodome.PublicKey import DSA as pycryptodomex_dsa
from Cryptodome.PublicKey import RSA as pycryptodomex_rsa
from Cryptodome.PublicKey import ECC as pycryptodomex_ecc
from os import urandom 

# --------- DSA TESTS -----------
# ruleid: weak-cryptographic-keys
dsa.generate_private_key(1024)

# ruleid: weak-cryptographic-keys
dsa.generate_private_key(key_size=1024, backends=backends.default_backend())

# ok: weak-cryptographic-keys
dsa.generate_private_key(key_size=2048, backend=backends.default_backend())

# ruleid: weak-cryptographic-keys
pycrypto_dsa.generate(1024)

# ruleid: weak-cryptographic-keys
pycrypto_dsa.generate(bits=1024, randfunc=urandom)

# ok: weak-cryptographic-keys
pycrypto_dsa.generate(2048)

# ruleid: weak-cryptographic-keys
pycryptodomex_dsa.generate(1024)

# ruleid: weak-cryptographic-keys
pycryptodomex_dsa.generate(bits=1024, randfunc=urandom)

# ok: weak-cryptographic-keys
pycryptodomex_dsa.generate(2048)


# ------------ RSA TESTS --------------
# ruleid: weak-cryptographic-keys
rsa.generate_private_key(public_exponent=65537, key_size=1024)

# Slightly wrong in the rule here, but luckily if 
# public exponent is smaller than 65537 it is a vulnerability
# ruleid: weak-cryptographic-keys
rsa.generate_private_key(public_exponent=3, key_size=1024, backend=backends.default_backend())

# ok: weak-cryptographic-keys
rsa.generate_private_key(public_exponent=65537, key_size=2048)

# ruleid: weak-cryptographic-keys
pycrypto_rsa.generate(bits=1024)

# ruleid: weak-cryptographic-keys
pycrypto_rsa.generate(bits=1024, randfunc=urandom)

# ok: weak-cryptographic-keys
pycrypto_rsa.generate(bits=2048)

# ruleid: weak-cryptographic-keys
pycryptodomex_rsa.generate(bits=1024)

# ruleid: weak-cryptographic-keys
pycryptodomex_rsa.generate(bits=1024, randfunc=urandom)

# ok: weak-cryptographic-keys
pycryptodomex_rsa.generate(bits=2048)


# ---------- ECC TESTS -------------
# ruleid: weak-cryptographic-keys
ec.generate_private_key(curve=ec.SECT233K1)

# ruleid: weak-cryptographic-keys
ec.generate_private_key(curve=ec.SECT163R2)

# ok: weak-cryptographic-keys
ec.generate_private_key(curve=ec.SECP256K1)

# ruleid: weak-cryptographic-keys
ec.generate_private_key(curve=ec.SECP224R1())

# ruleid: weak-cryptographic-keys
ec.generate_private_key(curve=ec.SECT163K1(), backend=backends.default_backend())

# ok: weak-cryptographic-keys
ec.generate_private_key(curve=ec.SECP256R1(), backend=backends.default_backend())

# ruleid: weak-cryptographic-keys
pycrypto_ecc.generate(curve='NIST P-192')

# ruleid: weak-cryptographic-keys
pycrypto_ecc.generate(curve="prime224v1", randfunc=urandom)

# ok: weak-cryptographic-keys
pycrypto_ecc.generate(curve='p256')

# ruleid: weak-cryptographic-keys
pycryptodomex_ecc.generate(curve='secp192r1')

# ruleid: weak-cryptographic-keys
pycrypto_ecc.generate(curve='P-224', randfunc=urandom)

# ok: weak-cryptographic-keys
pycrypto_ecc.generate(curve='secp256r1')


# --------- SYMBOLIC PROPAGATION ---------
some_key_size = 1024

# ruleid: weak-cryptographic-keys
rsa.generate_private_key(public_exponent=65537, key_size=some_key_size)

# ruleid: weak-cryptographic-keys
pycrypto_dsa.generate(some_key_size)

# ruleid: weak-cryptographic-keys
pycryptodomex_rsa.generate(bits=some_key_size)

