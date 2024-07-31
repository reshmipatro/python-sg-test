import httpx


# ok: 295-request-verify
httpx.request('GET', 'https://gmail.com', verify=True)
# ruleid: 295-request-verify
httpx.request('GET', 'https://gmail.com', verify=False)

# ok: 295-request-verify
httpx.get('https://gmail.com', verify=True)
# ruleid: 295-request-verify
httpx.get('https://gmail.com', verify=False)

# ok: 295-request-verify
httpx.options('https://gmail.com', verify=True)
# ruleid: 295-request-verify
httpx.options('https://gmail.com', verify=False)

# ok: 295-request-verify
httpx.head('https://gmail.com', verify=True)
# ruleid: 295-request-verify
httpx.head('https://gmail.com', verify=False)

# ok: 295-request-verify
httpx.post('https://gmail.com', verify=True)
# ruleid: 295-request-verify
httpx.post('https://gmail.com', verify=False)

# ok: 295-request-verify
httpx.put('https://gmail.com', verify=True)
# ruleid: 295-request-verify
httpx.put('https://gmail.com', verify=False)

# ok: 295-request-verify
httpx.patch('https://gmail.com', verify=True)
# ruleid: 295-request-verify
httpx.patch('https://gmail.com', verify=False)

# ok: 295-request-verify
httpx.delete('https://gmail.com', verify=True)
# ruleid: 295-request-verify
httpx.delete('https://gmail.com', verify=False)

# ok: 295-request-verify
httpx.stream('https://gmail.com', verify=True)
# ruleid: 295-request-verify
httpx.stream('https://gmail.com', verify=False)

# ok: 295-request-verify
httpx.Client()
# ruleid: 295-request-verify
httpx.Client(verify=False)

# ok: 295-request-verify
httpx.AsyncClient()
# ruleid: 295-request-verify
httpx.AsyncClient(verify=False)