#!/usr/bin/env python
import hashlib
from multiprocessing import Pool
import random
import time
__author__ = "William Koch"

'''
Brute forcer. Models a combination lock. Specify the lock search space, 
start position, max number of tries. 

TODO: Add kill hanlder same as done in the 
SSL side channel script so if killed will print the last one attempted so it 
can always be restarted at this point

'''
#class MD5PrefixFinder:

#    def __init__(self,prefix):
#        self.prefix = prefix

def find(a):
    prefix = "'||1#"
    p = chr(a)
    l = len(prefix)
    start = 33 # !
    end = 126 # ~
    i = 0
    pre = ''
    val = []
    m = hashlib.md5()
    while(True):

        s = p + str(i) 
        m.update(126)
        d = m.digest()
        if d[:l] == prefix:
            print d
            print '\n\n\n'
            print s
            break;
        i+=1
        if i%10000000 == 0:
            print s 
        #if i == end:
        #    i = start
        #else:
        #    i+=1
        #

def test(str):

    prefix = "'||1#"
    m = hashlib.md5()

    l = len(prefix)
    m.update(str)
    d = m.digest()
    if d[:l] == prefix:
        print str
        print d
        print '\n\n\n'
        return True
    else :
        return False


def toString(arr):
    base = 33
    s = ''
    for i in arr:
        s+=chr(base + i)
    return s


def rollover():

    size = 126 - 33
    start = 1
    arr = [start]

    i=0
    for i in range(1000):
#    while(True):

        l = len(arr)
            #shift
        rollover = False
        for j in range(l):
            
            #print str(i) + " " + str(j) 
            if arr[j]%size == 0:
                arr[j] = start # restart
                if ((j+1) < len(arr)):
                    #pass
                    arr[j+1]+=1
                    rollover = True
        #            print "Rollover!" + str(j)
                else:
                    arr.append(start)
                 
            else:
                if not(rollover):
                    arr[j]+=1
                break;
    
        s =  toString(arr) 
        print arr

        if i%10000000 == 0:
            print s 
        if test(s):
            break
        i+=1


if __name__ == "__main__":
#    pool = Pool(processes=8)
#    pool.map(find,range(33,126))
# #   pool.close()
#    pool.join()
#    md5prefix = MD5PrefixFinder(prefix)
#    md5prefix.find()
#    find(33)
    rollover()
