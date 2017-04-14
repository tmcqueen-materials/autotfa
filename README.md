# AutoTFA
Passwordless/Automatic Logins on Sites Using TOTP/HOTP Two Factor Authentication (MAgic Remote Control of Commands: MARCC)

This page describes how to implement automated/programmatic/passwordless access to a resource protected with TOTP/HOTP two factor authentication (TFA), such as that found in Google Authenticator. It is based on a variety of web sources.


SECURITY NOTE: These instructions should only be used in cases where you are unable to setup proper key-based authentication with a passphrase-protected secret key, or better, as it reduces the security to the equivalent of using key-based authentication with no passphrase. You should also make sure that it does not violate any terms of service that you have agreed to. These instructions were originally written to deal with a buggy remote system that requested TFA when no TFA was required for that login type.


There are two steps to implementing automatic access:

1. Convert the shared secret QR code (the image that is displayed to setup TFA) to a URL. It will have the general form (from ref. 1 below):
   otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example
2. Use the shared secret combined with an implementation of a TOTP/HOTP code generator to automatically generate and supply the necessary TFA code.

There are many ways to accomplish these two steps.


Generic Example:

1. Download and Install ZBar (ref. 2 below), an open source QR code reader/decoder.
2. Save the QR Code as an image from the site that generated it.
3. Decode the QR Code by running zbarimg <image-file>. The relevant parameters are the type (totp in the example above) and the shared secret (JBSWY3DPEHPK3PXP in the example above). If the type is hotp, the third relevant parameter is the number after counter= (not present in above example which is not hotp).
4. Install the onetimepass python module: pip install onetimepass (or, if a system installation, prefix with sudo).
5. Write a small python script to generate the TFA code, save it as a file, e.g. ~/genTFA.py (from ref. 3 below), and mark it executable, e.g. chmod 700 ~/genTFA.py. For totp (most common):
   #!/usr/bin/python
   import onetimepass as otp
   my_secret = 'JBSWY3DPEHPK3PXP'
   my_token = otp.get_totp(my_secret)
   print my_token
6. If the type is hotp, it is slightly more complicated. You must replace get_totp(my_secret) with get_hotp(my_secret, interval_no=my_counter). You then need to add the appropriate lines to set my_counter to the value of counter from the QR code, incrementing it each time getTFA.py is called. Usually this means storing the current counter in a separate file, reading it into my_counter, calculating the hotp code, incrementing the my_counter, and then saving the updated counter back to the file for the next use.
7. Congratulations, you can now use the output of genTFA.py to automatically login to a site with TFA. For example, for a Password+TFA protected SSH connection, you can do (all one line):
   ~/genTFA.py > pwfile; echo "Your Password" >> pwdfile; sshpass -t -fpwfile ssh -l <user-id> <TheServer> <command-on-remote-server>
   You need to compile and use the version of sshpass here that includes TFA support. For an interactive session, leave off <command-on-remote-server>. If the server requests the password before the TFA code, you can change the command to:
   echo "Your Password" > pwdfile; ~/genTFA.py >> pwfile; sshpass -t -fpwfile ssh -l <user-id> <TheServer> <command-on-remote-server>
As an alternative to the TFA enabled sshpass, you can use expect.

Pure Python Example:

1. Retreive your TFA secret key: login to the system by normal means and run cat ~/.google_authenticator. The 16 character secret is the first line of the output, e.g. JBSWY3DPEHPK3PXP. Then logout of the system (the rest of the steps must be done on your local computer).
2. Install the onetimepass python module: pip install onetimepass (or, if a system installation, prefix with sudo).
3. Save the python script ssh-tfa.py in your home directory and mark it exeuctable, e.g. chmod 700 ~/ssh-tfa.py.
4. Edit the python script, replace secret with the one you found in step 1, and add your password.
5. Congratulations, you can now use ~/ssh-tfa.py anywhere you would use the ssh command. For example:
   ~/ssh-tfa.py -X <The-Server> -l <user-id>
NOTE:Due to limitations of the current python script, some actions (e.g. screen resizing) do not work as you might expect. If this is a problem, use the generic example and custom sshpass instead.

References

1. https://github.com/google/google-authenticator/wiki/Key-Uri-Format
2. http://zbar.sourceforge.net/
3. https://github.com/tadeck/onetimepass
4. https://github.com/LazarSoft/jsqrcode

