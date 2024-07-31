from paramiko import client

ssh_client = client.SSHClient()

# ruleid: 322-sshclient-host-key-policy
ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())

# ruleid: 322-sshclient-host-key-policy
ssh_client.set_missing_host_key_policy(client.WarningPolicy())

# ok: 322-sshclient-host-key-policy
ssh_client.set_missing_host_key_policy(client.RejectPolicy())

def func(ssh_client: paramiko.client.SSHClient):
    # ruleid: 322-sshclient-host-key-policy
    ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
    return 1

def func2(ssh_client):
    # todoruleid: 322-sshclient-host-key-policy
    ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
    return 1
