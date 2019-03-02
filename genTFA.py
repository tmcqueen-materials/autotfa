#!/usr/bin/python3
import sys
import onetimepass as otp
my_secret = sys.argv[1]
my_token = otp.get_totp(my_secret)
print(format(my_token,'06d'))

