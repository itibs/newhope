#!/usr/bin/python

from pwn import *
from newhope import Polynomial

import pdb

PARAM_Q = 12289
PARAM_K = 16
PARAM_N = 1024

def main():
    io = process('test/test_newhope')
    # read a
    io.recvline()
    line = io.recvline()
    a_coeff = [int(x) for x in line.split(" ") if x <> '\n']
    a = Polynomial()
    a.set_coeff(a_coeff)
    # read sk
    io.recvline()
    sk_coeff = [int(x) for x in io.recvline().split(" ") if x <> '\n']
    sk = Polynomial()
    sk.set_coeff(sk_coeff)
    # read b
    io.recvline()
    b_coeff = [int(x) for x in io.recvline().split(" ") if x <> '\n']
    b = Polynomial()
    b.set_coeff(b_coeff)

    s = get_s(a, b)

    print "their s" + str(sk)
    print "myown s" + str(s)

    good = 0
    bad = 0
    for i in xrange(PARAM_N):
        if sk.coeff[i] == s.coeff[i]:
            good += 1
        else:
            bad += 1
            print str(sk.coeff[i]) + " - " + str(s.coeff[i])

    print "percentage: " + str(float(good) / (float(good) + float(bad)) * 100)

def get_sk(a, b):
    res = []
    for i in xrange(PARAM_K + 1):
        ik = i + PARAM_Q - PARAM_K / 2
        for j in xrange(PARAM_K + 1):
            jk = j + PARAM_Q - PARAM_K / 2
            if ((a * ik) + jk) % PARAM_Q == b:
                res.append(ik)
                return ik

    if len(res) > 1:
        print res

    return -1

def get_s(a, b):
    s_coeff = []
    for k in xrange(PARAM_N):
        ak = a.coeff[k]
        bk = b.coeff[k]
        s_coeff.append(get_sk(ak, bk))

    s = Polynomial()
    s.set_coeff(s_coeff)

    return s

if __name__ == "__main__":
    main()
