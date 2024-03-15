'''
In this file we find a function that uses the vulnerable
pycrypto dependency and its ARC2 module in its version 2.0.1.

Description: Buffer overflow in the PyCrypto ARC2 module 2.0.1 allows
remote attackers to cause a denial of service and possibly execute
arbitrary code via a large ARC2 key length.

Vulnerability: https://nvd.nist.gov/vuln/detail/CVE-2009-0544
Exploit: https://www.exploit-db.com/exploits/32780
'''

from Crypto.Cipher import ARC2
from Crypto import Random

key = b'Sixteen byte key'
iv = Random.new().read(ARC2.block_size)
cipher = ARC2.new(key, ARC2.MODE_CFB, iv)
msg = iv + cipher.encrypt(b'Attack at dawn')
