import pexpect
import sys, time
cmdlist = ['cat /tmp/sn','cat /tmp/erm/version','iwpriv ra0 copy_to_user devinfo', 'iwpriv ra0 copy_to_user devinfo']
results = []
hlogin = '192.168.225.1'

for items in cmdlist:
    dev1 = pexpect.spawn('telnet {}'.format(hlogin))
    dev1.logfile = sys.stdout.buffer
    dev1.expect('tc login:')
    dev1.sendline('admin')
    dev1.expect('Password:')
    dev1.sendline('admin')
    dev1.expect('#')
    dev1.sendline('{}'.format(items))
    dev1.expect('#',timeout=100)
    x = dev1.before.decode('utf-8').splitlines()
    results.append(x)
    dev1.sendline('exit')
print(results)