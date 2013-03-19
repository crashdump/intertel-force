#!/usr/bin/env python

__doc__ = """The Inter-Tel password is a digit only password. From 0 to 8 digits.
Used with a pwdrange of 10000 it will generate all the numbers from 0000...0001 to 9999."""

pwdrange = 10000

f = open('pwd.txt', 'r+')
for n in ["%04d" % x for x in range(pwdrange)]:
    f.write('%s\r\n' % n)

f.close()
