'''
Script Name     :Firmware Sanity Test For Platform CLI Output Validation
Owner           :Youvanes
Contact         :youvanesp@embedur.com
Total TC        :14

Run Command     :python3 <script_name> <cmdlist_file> <script_id> 
script_name     :script file
cmdlist_file    :Below command list saved to a file
script_id       :Either give one TC_ID or multiple
                 ex: single:    1
                     multiple:  1,2,3
    
#Below Commands are validated based on request from dev team,
1.cat /tmp/sn
2.cat /tmp/erm/version
3.cat /tmp/fw_ver
4.iwpriv ra0 copy_to_user devinfo
5.iwpriv rai0 copy_to_user devinfo
6.iwpriv ra0 copy_to_user statinfo
7.iwpriv rai0 copy_to_user statinfo
8.iwpriv ra0 copy_to_user get_stalist
9.iwpriv rai0 copy_to_user get_stalist
10.iwpriv apclii0 copy_to_user devconnStatus
11.iwpriv ra0 copy_to_user clientcountinfo
12.iwpriv ra0 copy_to_user clientinfo
13.iwpriv ra0 copy_to_user get_stainfo=24G_TEST_CLIENT
14.iwpriv rai0 copy_to_user get_stainfo=5G_TEST_CLIENT

Link to Request:
https://teams.microsoft.com/l/entity/com.microsoft.teamspace.tab.wiki/tab::0d135496-3fa6-40ff-a1c7-3656664a88ff?context=%7B%22subEntityId%22%3A%22%7B%5C%22pageId%5C%22%3A49%2C%5C%22sectionId%5C%22%3A89%2C%5C%22origin%5C%22%3A2%7D%22%2C%22channelId%22%3A%2219%3Ac905dfaf8b194b438afa96e1fc59b847%40thread.skype%22%7D&tenantId=3e7c9d67-afab-4694-94e1-af28129ed65f

'''
import pexpect
import inspect
import time, sys, os
import fileinput
from shutil import copyfile
from datetime import date
from datetime import datetime


def main():                   
    filepath = sys.argv[1]
    scriptid = sys.argv[2]
    #filepath1 = "cmd_list_clients_temp"
    #copyfs = filecpy(filepath,filepath1)
    #print("File Copy Status: {}".format(copyfs))
    cmdname = ['Device_SN','ERM_VERSION','FIRMWARE_VERSION','24G_RA0_DEVINFO','5G_RAI0_DEVINFO','24G_RA0_STATINFO','5G_RAI0_STATINFO','24G_RA0_GET_STA_LIST','5G_RAI0_24G_RA0_GET_STA_LIST','WLM_APCLII0_DEVCONNSTATUS','24G_RA0_CLICOUNT','24G_RA0_CLI_INFO','24G_STA_INFO','5G_STA_INFO','24G_C2USR_RSTAT','24G_C2USR_MBSS','5G_C2USR_MBSS']
    print(cmdname)
    hlogin = '192.168.225.1'
    hlogin2 = '192.168.225.7'
    script_count=0
    aclstr = "5G_TEST_CLIENT"
    bclstr = "24G_TEST_CLIENT"
    bclient = '80:5E:4F:A8:90:2D'
    aclient = '08:71:90:1b:31:6d'
    cmdin = []
    cmdout = []
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    opdir_n = time.ctime().split()[1]+"_"+time.ctime().split()[2]+"_"+time.ctime().split()[3]
    print(path)
    oppath = path+"/"+"output"
    opdir = oppath+"/"+opdir_n
    if os.path.isdir(oppath):
        os.mkdir(opdir)
        if os.path.isdir(opdir):
            print("Results are stored at dir \n {} \n {}".format(oppath, opdir))
    else:
        os.mkdir(oppath)
        os.mkdir(opdir)
        if os.path.isdir(opdir):
            print("Results are stored at directory \n {} \n {}".format(oppath, opdir))
    
    
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    
    with open(filepath) as fp:
        cnt = 0
        for line in fp:
            cmdline = line.strip('\n')
            if aclstr in cmdline:
                cmdline1 = cmdline.replace(aclstr,aclient)
                print("a client updated to cmdlist")
                cmdin.append(cmdline1)
            elif bclstr in cmdline:
                cmdline2 = cmdline.replace(bclstr,bclient)
                print("b client updated to cmdlist")
                cmdin.append(cmdline2)
            else:
                cmdin.append(cmdline)
    #print(cmdin)
    #convert input specific script id's
    hyp = "-"
    comma = ","
    tcno = []
    
    if hyp in scriptid: 
        print("hyphen detected")
        tcno = scriptid.split(hyp)
    elif comma in scriptid:
        print("comma detected")
        tcno = scriptid.split(comma)
    elif len(scriptid) == 1 or len(scriptid) == 2:
        tcno.append(scriptid)
    elif "all" in scriptid:
        print("Full script is executed")
    else:
        print("Third arg input is undetermined, so default run triggered")
    print(tcno)
    
    if tcno:
        newcmdin = []
        newcmdname = []
        for items in tcno:
            newcmdin.append(cmdin[int(items)-1])
            newcmdname.append(cmdname[int(items)-1])
        print(newcmdin)
        print(newcmdname)
        cmdin = newcmdin
        cmdname = newcmdname
    print(cmdin)
    print(cmdname)
    for items in cmdname:
        if items.split("_")[0] == "WLM":
            print("Runs for Wireless Mesh Node")
            dev2 = pexpect.spawn('telnet {}'.format(hlogin2))
            dev2.logfile = sys.stdout
            filen = "TC_ID_{}_{}.log".format(script_count+1,cmdname[script_count])
            filename = opdir+"/"+filen            
            dev2.logfile = open(filename, 'wb')
            dev2.expect('tc login:')
            dev2.sendline('admin')
            dev2.expect('Password:')
            dev2.sendline('admin')
            dev2.expect('#')
            dev2.sendline('{}'.format(cmdin[script_count]))
            dev2.expect('#',timeout=100)
            dev2.sendline('exit')
            dev2.logfile.close()
            script_count=script_count+1        
        else:
            dev1 = pexpect.spawn('telnet {}'.format(hlogin))
            dev1.logfile = sys.stdout
            filen = "TC_ID_{}_{}.log".format(script_count+1,cmdname[script_count])
            filename = opdir+"/"+filen            
            dev1.logfile = open(filename, 'wb')
            dev1.expect('tc login:')
            dev1.sendline('admin')
            dev1.expect('Password:')
            dev1.sendline('admin')
            dev1.expect('#')
            dev1.sendline('{}'.format(cmdin[script_count]))
            dev1.expect('#',timeout=100)
            dev1.sendline('exit')
            dev1.logfile.close()
            script_count=script_count+1
    print(cmdout)

def filecpy(srcf,archf):
    #Proc to copy files written from the logging to the archive path
    try:
        copystatus=copyfile(srcf,archf)
        print("Temp file copied:\t {}".format(archf))
        return True
    except IOError as e:
        print("Unable to copy file. %s" % e)
        return False
    except:
        print("Unexpected error:", sys.exc_info())
        return False

            
if __name__ == '__main__':
    main()

