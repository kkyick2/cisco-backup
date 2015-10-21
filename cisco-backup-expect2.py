#!/usr/bin/python
import pexpect
import sys
import time
import datetime

class CiscoSwitch():

    def __init__(self, host, username, password):
        self.username = username
        self.host = host
        self.password = password

    def Login(self):
        self.child = pexpect.spawn('telnet '+self.host)
        self.child.expect('Username:')
        self.child.sendline(self.username)
        self.child.expect('Password:')
        self.child.sendline(self.password)
        self.child.expect('#')
        self.child.sendline('terminal length 0')
        self.child.expect('#')
        return (self.child, self.child.before)

    def RunShowCmd(self,cmd):
        self.child.sendline(cmd)
        self.child.expect('#')
        return (self.child, self.child.before)

    def FtpBackupCmd(self,ftpip):
        self.child.sendline('copy running-config ftp:')
        self.child.expect(']?')
        self.child.sendline(ftpip)
        self.child.expect(']?')
        DATE = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        self.child.sendline(DATE+'-'+self.host)
        self.child.expect('#')
        return (self.child, self.child.before)

if __name__ == '__main__':

        now = datetime.datetime.now()
        filename_prefix = 'cisco-backup'
        host = '172.22.24.249'

        filename = "%s_%s_%.2i-%.2i-%i_%.2i-%.2i-%.2i" % (filename_prefix,host,now.day,now.month,now.year,now.hour,now.minute,now.second)

        fp=open(filename,"w")

        print 'This program is being run by itself'
        Switch = CiscoSwitch('172.22.24.249','wttadmin','col123col')
        (obj,stdout) = Switch.Login()
        print stdout
        fp.write(stdout)

        (obj,stdout) = Switch.RunShowCmd('show run')
        print stdout
        fp.write(stdout)

        (obj,stdout) = Switch.RunShowCmd('show ip int brief')
        print stdout
        fp.write(stdout)

        fp.close()

 #       (obj,stdout) = Switch.FtpBackupCmd('1.1.1.1')
 #       print stdout
ဥ
