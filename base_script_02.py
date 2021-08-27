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
    script_start = time.time()
    cmdname = ['Device_SN','ERM_VERSION','FIRMWARE_VERSION','24G_RA0_DEVINFO','5G_RAI0_DEVINFO','24G_RA0_STATINFO','5G_RAI0_STATINFO','24G_RA0_GET_STA_LIST','5G_RAI0_24G_RA0_GET_STA_LIST','APCLII0_DEVCONNSTATUS','24G_RA0_CLICOUNT','24G_RA0_CLI_INFO','24G_STA_INFO','5G_STA_INFO']
    print(cmdname)
    hlogin = '192.168.25.1'
    script_count=0
    aclstr = "5G_TEST_CLIENT"
    bclstr = "24G_TEST_CLIENT"
    bclient = '80:5E:4F:A8:90:2D'
    aclient = '08:71:90:1b:31:6d'
    cmdin = []
    cmdout = []
    res_tab_def = ['Test_ID_CNT', 'TC_DESC', 'TRESULTS_NA', 'HYPER_LINK']
    res_tab_info = ['SCRPT_LOC_NA','RUNTIME_NA','TC_PATH_NA']
    tcresdef = ['Total_TC_NA','PASS_COUNT_NA','FAIL_COUNT_NA']
    htmltccode1 = '''-Completed-'''
    htmltccode2 = '''<tr><td>Test_ID_CNT</td><td><a href="HYPER_LINK">TC_DESC</a></td><td>TRESULTS_NA</td></tr>-Completed-'''
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    opdir_n = time.ctime().split()[1]+"_"+time.ctime().split()[2]+"_"+time.ctime().split()[3]
    print(path)
    respath1 = path+"/"+"result1.html"
    
    
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
    print(cmdin)
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
    elif len(scriptid) == 1:
        tcno.append(scriptid)
    elif "all" in scriptid:
        print("Full script is executed")
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
    #below assignment for creating a template of html file @ output dir
    respath2 = opdir+"/"+"results.html"
    filecopy = filecpy(respath1,respath2)
    #print("filecopy step: {}".format(filecopy))
    #List to maintatin pass fail stats
    tcres1 = []
    #for loop to continously trigger telnet for each command and log into output dir seperately
    print(cmdin)
    print(cmdname)
    for items in cmdin:
        res_tab_tar = []
        res_tab_res = 'FAIL'
        #Code for telnet and logging into file
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
        dev1.sendline('{}'.format(items))
        dev1.expect('#',timeout=100)
        dev1.sendline('exit')
        dev1.logfile.close()
        res_tab_tar.append("TC_ID_{}".format(script_count+1))
        res_tab_tar.append(cmdname[script_count])
        res_tab_tar.append(res_tab_res)
        res_tab_tar.append(filen)
        print(res_tab_tar)
        proc_to_rep1 = strch(respath2, htmltccode1, htmltccode2)
        print(proc_to_rep1)
        tcount = 0
        tcp = 0
        tcf = 0
        for results in res_tab_tar:
            proc_to_rep2 = strch(respath2, res_tab_def[tcount], results)
            #print("replace proc:{}: {}".format(tcount+1,proc_to_rep))
            tcount = tcount + 1
            if results == 'PASS':
                tcp = tcp+1
            elif results == 'FAIL':
                tcf = tcf+1
            tcres1.append(script_count+1)
            tcres1.append(tcp)
            tcres1.append(tcf)
            tc1 = 0
            for results in tcres1:
                proc_to_rep = strch(respath2, str(tcresdef[tc1]), str(results))
                print("results one {},{}".format(tcresdef[tc1],results))
                tc1 = tc1 + 1        
    res_new_info = []
    fscriptname = os.path.realpath(__file__)
    res_new_info.append(fscriptname.split("/")[-1])
    timeinsecs=time.time() - script_start
    timew = secondsToText(timeinsecs)
    res_new_info.append(timew)
    res_new_info.append(opdir)
    tcount = 0
    for results in res_new_info:
        proc_to_rep = strch(respath2, res_tab_info[tcount], results)
        tcount = tcount + 1       
def filecpy(srcpath,tpath):
    #Proc to copy files written from the logging to the archive path
    try:
        copystatus=copyfile(srcpath,tpath)
        print("{} file copied:\t {}".format(srcpath, tpath))
        return True
    except IOError as e:
        print("Unable to copy file. %s" % e)
        return False
    except:
        print("Unexpected error:", sys.exc_info())
        return False

def strch(resf, srcstr,copystr):
    # find and replace the file in html for mailing input
    text_to_search = srcstr
    replacement_text = copystr
    count = 0
    print ("HTML FILE is being modified")
    print(resf)
    print(srcstr)
    print(copystr)  
    with fileinput.FileInput(resf, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(text_to_search, replacement_text), end='')

def secondsToText(secs):
    days = secs//86400
    hours = (secs - days*86400)//3600
    minutes = (secs - days*86400 - hours*3600)//60
    seconds = secs - days*86400 - hours*3600 - minutes*60
    result = ("{0} day{1}, ".format(days, "s" if days!=1 else "") if days else "") + \
    ("{0} hour{1}, ".format(hours, "s" if hours!=1 else "") if hours else "") + \
    ("{0} minute{1}, ".format(minutes, "s" if minutes!=1 else "") if minutes else "") + \
    ("{0} second{1}, ".format(seconds, "s" if seconds!=1 else "") if seconds else "")
    return result
if __name__ == '__main__':
    main()

