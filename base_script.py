import pexpect
import sys

dev1 = pexpect.spawn('telnet 192.168.225.1')
dev1.logfile = sys.stdout.buffer
dev1.expect('tc login:')
dev1.sendline('admin')
dev1.expect('Password:')
dev1.sendline('admin')
dev1.expect('#')
dev1.sendline('cat /tmp/sn')
dev1.expect('#')
dev1.sendline('cat /tmp/erm/version')
dev1.expect('#')
x = dev1.before.decode('utf-8').splitlines()
print(x)
print("=====FORMAT_OUTPUT==========")
for line in x:
    print(line)
