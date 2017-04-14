#!/usr/bin/python
import pty
import sys
import os
import onetimepass as otp

secret = 'JBSWY3DPEHPK3PXP'
password = 'Your Password'

tfadone = 0
pwdone = 0

def read(fd):
	global tfadone, pwdone, secret, password
	data = os.read(fd, 1024)
	if tfadone and pwdone:
		return data
	lower = data.lower()
	if not pwdone and 'password:' in lower:
		os.write(fd, password + '\n');
		pwdone = 1
		return ''
	elif not tfadone and 'code:' in lower:
		os.write(fd, str(otp.get_totp(secret)) + '\n');
		tfadone = 1
		return ''
	else:
		return data

sshcmd = sys.argv
sshcmd[0] = '/usr/bin/ssh'

pty.spawn(sshcmd,read)

