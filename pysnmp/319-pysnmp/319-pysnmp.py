from pysnmp.hlapi import UsmUserData

# ruleid: 319-pysnmp
insecure = pysnmp.hlapi.UsmUserData("securityName")

# ruleid: 319-pysnmp
auth_no_priv = UsmUserData("securityName",'authName')

# ruleid: 319-pysnmp
auth_no_priv = UsmUserData("securityName",authKey='myauthkey')

# ok: 319-pysnmp
less_insecure = UsmUserData("securityName","authName","privName")

# ok: 319-pysnmp
secure = pysnmp.hlapi.UsmUserData('testuser', authKey='myauthkey', privKey='myenckey')