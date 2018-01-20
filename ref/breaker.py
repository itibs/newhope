#!/usr/bin/python

from pwn import *
import itertools
from newhope import Polynomial

import pdb

PARAM_Q = 12289
PARAM_K = 20
PARAM_N = 1024

VERBOSE = False

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
    diff_s(s, sk)

    guesses = 0
    found = False

    for s in get_all_s(a, b):
        if -1 in s.coeff:
            break
        guesses += 1
        if cmp_s(s, sk):
            print "FOUND %d guesses" % guesses
            found = True
            break

    if not found:
        print "NOT_FOUND %d guesses" % guesses

def diff_s(s, sk):
    if VERBOSE:
        print "their s" + str(sk)
        print "myown s" + str(s)

    good = 0
    bad = 0
    for i in xrange(PARAM_N):
        if sk.coeff[i] == s.coeff[i]:
            good += 1
        else:
            bad += 1
            if VERBOSE:
                print str(sk.coeff[i]) + " - " + str(s.coeff[i])

    if VERBOSE:
        print "percentage: " + str(float(good) / (float(good) + float(bad)) * 100)

def cmp_s(s, sk):
    diff = [(s.coeff[i], sk.coeff[i], i) for i in xrange(PARAM_N) if s.coeff[i] != sk.coeff[i]]
    if len(diff) == 0:
        return True

    return False

def get_s_coeff(a, b):
    res = []
    for i in xrange(PARAM_K + 1):
        ik = i + PARAM_Q - PARAM_K / 2
        for j in xrange(PARAM_K + 1):
            jk = j + PARAM_Q - PARAM_K / 2
            if ((a * ik) + jk) % PARAM_Q == b % PARAM_Q:
                res.append(ik)
                #return ik

    if len(res) > 0:
        if VERBOSE and len(res) > 1:
            print res
        return res, len(res)

    return [-1], 1

def get_s(a, b):
    s_coeff = []
    combinations = 1
    for k in xrange(PARAM_N):
        ak = a.coeff[k]
        bk = b.coeff[k]
        coeff, nr = get_s_coeff(ak, bk)
        s_coeff.append(coeff[0])
        combinations *= nr

    if VERBOSE:
        print combinations
    s = Polynomial()
    s.set_coeff(s_coeff)

    return s

def get_all_s(a, b):
    s_coeffs = []
    combinations = 1
    for k in xrange(PARAM_N):
        ak = a.coeff[k]
        bk = b.coeff[k]
        coeff, nr = get_s_coeff(ak, bk)
        s_coeffs.append(coeff)
        combinations *= nr

    print combinations

    for s_coeff in itertools.product(*s_coeffs):
        s = Polynomial()
        s.set_coeff(s_coeff)
        yield s

    return

if __name__ == "__main__":
    main()
