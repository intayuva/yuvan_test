import pexpect
import sys, time
cmdlist = ['cat /tmp/sn','cat /tmp/erm/version','iwpriv ra0 copy_to_user devinfo', 'iwpriv ra0 copy_to_user devinfo']
results = []
hlogin = '192.168.225.1'
dev1 = pexpect.spawn('telnet {}'.format(hlogin))
dev1.logfile = sys.stdout.buffer
dev1.expect('tc login:')
dev1.sendline('admin')
dev1.expect('Password:')
dev1.sendline('admin')
dev1.expect('#')

for items in cmdlist:
    dev1.sendline('{}'.format(items))
    dev1.expect('#',timeout=100)
   
    #print("-------{}-------\n".format(x[0]))
    #x = x.pop(0)
    #print(str(x.index(line))+" "+line)
    #print("CLI Command: "+ x[0] +" "+"=>")
    #print(x)
    #print("-------EoC-------\n")
