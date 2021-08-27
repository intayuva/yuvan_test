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
import subprocess
from shutil import copyfile
from datetime import date
from datetime import datetime


def main():                   
    filepath = sys.argv[1]
    scriptid = sys.argv[2]
    #filepath1 = "cmd_list_clients_temp"
    #copyfs = filecpy(filepath,filepath1)
    #print("File Copy Status: {}".format(copyfs))
    cmdname = ['Device_SN','ERM_VERSION','FIRMWARE_VERSION','24G_RA0_DEVINFO','5G_RAI0_DEVINFO','24G_RA0_STATINFO','5G_RAI0_STATINFO','24G_RA0_GET_STA_LIST','5G_RAI0_GET_STA_LIST','24G_RA0_GET_STA_LIST','WLM_APCLII0_DEVCONNSTATUS','24G_RA0_CLICOUNT','24G_RA0_CLI_INFO','24G_STA_INFO','5G_STA_INFO','5G_C2USR_RSTAT','24G_C2USR_MBSS','5G_C2USR_MBSS']
    cmdres = []
    print(cmdname)
    hlogin = '192.168.1.1'
    hlogin2 = '192.168.1.4'
    script_count=0
    aclstr = "5G_TEST_CLIENT"
    bclstr = "24G_TEST_CLIENT"
    bclient = '80:5E:4F:A8:90:2D'
    aclient = '08:71:90:1b:31:6d'
    #bclient = '6e:17:9a:f8:21:b5'
    #aclient = '08:71:90:1B:31:6D'
    cmdin = []
    cmdout = []
    
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    opdir_n = time.ctime().split()[1]+"_"+time.ctime().split()[2]+"_"+time.ctime().split()[3]
    print(path)
    oppath = path+"/"+"output"
    bmarkd = path+"/"+"benchmark"+"/"+"GPON"
    print(bmarkd)
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
            filen = filename.split("/")[-1].split("_")
            filen2 = "_".join(filen[3:])
            bfilename = bmarkd+"/"+filen2
            print(bfilename)
            if os.path.isfile(bfilename):
                filecr = filecomp(bfilename,filename,opdir)
                cmdres.append(filecr)
            else:
                print("benchmark file missing")
    print(cmdout)
    print(cmdname)
    print(cmdres) 
    for tccount1 in range(len(cmdres)):
        print("TC:{}\t -\t {} \t \t {}  ".format(tccount1+1,cmdname[tccount1],cmdres[tccount1]))
        tccount1+1
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

def filecomp(file1,file2, odir):
    cnt = 0
    results = []
    spcharrs = []
    eq1 = "="
    col1 = ":"
    spchar = ['=','-',':']
    bfilename = file2.split("/")[-1]
    for items in spchar:
        gcmd = '''grep {} {} | wc -l '''.format(items,file1)
        eqc = subprocess.check_output(gcmd,shell=True)
        print(eqc)
        gcmd1 = '''grep {} {} | wc -l '''.format(items,file2)
        eqc1 = subprocess.check_output(gcmd1,shell=True)
        print(eqc1)
        reseq = eqc == eqc1
        if reseq:
            print("PASS:{} ...Special Char Count PASSED".format(items))
            resq1="PASSED"
        else:
            print("FAIL: {} ...Special_Char COUNT FAILED".format(items))
            resq1="FAILED"
        spcharrs.append(resq1)
    new1="/".join(spcharrs)
    print("TC:{}\t -\t".format(bfilename)+new1)
        
    with open(file1, 'r') as f1:
        with open(file2, 'r') as f2:
            
            file1list = f1.read().splitlines()[8:]
            file2list = f2.read().splitlines()[8:]
            list1length = len(file1list)
            print(list1length)
            
            list2length = len(file2list)
            print(list2length)
            if list1length == list2length:
                while cnt < len(file1list):
                    str1 = file1list[cnt]
                    str2 = file2list[cnt]
                    if eq1 in str1: 
                        inx = str1.index(eq1)
                        fstr1 = str1[0:inx+1].strip()
                        fstr2 = str2[0:inx+1].strip()
                    elif col1 in str1:
                        inx = str1.index(col1)
                        fstr1 = str1[0:inx+1].strip()
                        fstr2 = str2[0:inx+1].strip()                    
                    else:
                        fstr1 = str1
                        fstr2 = str2
                    if fstr1 == fstr2:
                        lcom = "PASS"    
                    else:
                        lcom = "FAIL"
                        results.append(fstr2+"_"+"FAIL")
                    print(" | "+str1+"\t \t \t \t"+" | "+"" +str2+"\t \t \t \t"+ lcom)
                   
                    compfile = odir+"/"+"compare_results"+".log"
                    print(compfile)
                    file1 = open(compfile, "a+")
                    #file1.write("-------- START of Script:{} --------\n".format(bfilename))
                    file1.write(" | "+str1+"\t \t \t \t"+" | "+"" +str2+"\t \t \t \t"+ lcom+"\n")
                    #file1.write("-------- END of Test for current CLI Command --------\n")
                    file1.close()
                    cnt = cnt + 1
            else:
                results.append("COL_FAIL") 
    if results:
        print(col1.join(results))
        x = col1.join(results)
        return x
    else:
        print("TRUE")
        return True

            
if __name__ == '__main__':
    main()

