# SNMP v3arch
from pysnmp.hlapi import CommunityData

# ruleid: 319-snmp-version
a = CommunityData('public', mpModel=0)

# ruleid: 319-snmp-version
a = CommunityData('public', mpModel=1)

# SNMP v1arch
from pysnmp.hlapi.v1arch import CommunityData as CD
# ruleid: 319-snmp-version
a = CD('public')

# ok: 319-snmp-version
secure = pysnmp.hlapi.UsmUserData('testuser', authKey='myauthkey', privKey='myenckey')