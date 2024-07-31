import requests

# ok: 295-request-verify
requests.get('https://gmail.com', timeout=30, verify=True)
# ruleid: 295-request-verify
requests.get('https://gmail.com', timeout=30, verify=False)

# ok: 295-request-verify
requests.post('https://gmail.com', timeout=30, verify=True)
# ruleid: 295-request-verify
requests.post('https://gmail.com', timeout=30, verify=False)

# ok: 295-request-verify
requests.put('https://gmail.com', timeout=30, verify=True)
# ruleid: 295-request-verify
requests.put('https://gmail.com', timeout=30, verify=False)

# ok: 295-request-verify
requests.delete('https://gmail.com', timeout=30, verify=True)
# ruleid: 295-request-verify
requests.delete('https://gmail.com', timeout=30, verify=False)

# ok: 295-request-verify
requests.patch('https://gmail.com', timeout=30, verify=True)
# ruleid: 295-request-verify
requests.patch('https://gmail.com', timeout=30, verify=False)

# ok: 295-request-verify
requests.options('https://gmail.com', timeout=30, verify=True)
# ruleid: 295-request-verify
requests.options('https://gmail.com', timeout=30, verify=False)

# ok: 295-request-verify
requests.head('https://gmail.com', timeout=30, verify=True)
# ruleid: 295-request-verify
requests.head('https://gmail.com', timeout=30, verify=False)
