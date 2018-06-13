
import subprocess
import platform
import re

def runcmd(cmd,args=''):
    if args != '':
        cmd = "[%s,%s]"%(cmd,args)
    #print cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.decode().split('\n')

def getnetworkip():
    os = platform.system()
    ip = ''
    if os == 'Darwin' or os =='Linux':
        cmd = "ifconfig"
    else:
        cmd = "ipconfig"
    ipArray = runcmd(cmd)
    isFind = 0
    #print ipArray
    for idstring in ipArray:
        #print "==="+idstring+"===="
        isLocal = idstring.find('127.0.0.1')
        #validateip = re.match('^(([01]?\d?\d|2[0-4]\d|25[0-5])\.){3}([01]?\d?\d|2[0-4]\d|25[0-5])\/(\d{1}|[0-2]{1}\d{1}|3[0-2])$', idstring)
        isnetip = idstring.find('inet')
        # if isnetip != -1:
        #     print "ok1"+idstring
        if isLocal != -1:
            continue

        if isnetip != -1:
            #print "validate:==="+idstring
            validateArray = idstring.split(' ')
            #print validateArray
            for item in validateArray:
                #print item
                item  = item.replace('addr:','')
                pat = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
                matchstring = pat.match(item)
                #print item+"****"+str(matchstring)
                if matchstring != None:

                    ip = item
                    isFind = 1
                    break

        if isFind==1:
            break
    return ip

if __name__ == '__main__':
    print("host ip: "+getnetworkip())
