# -*- coding: utf-8 -*-
import re, string, random, glob, operator, heapq, os
from collections import defaultdict
from math import log10

def memo(f):
    "Memoize function f."
    table = {}
    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]
    fmemo.memo = table
    return fmemo

################ Word Segmentation

@memo
def segment(text):
    "Return a list of words that is the best segmentation of text."
    #text=text.decode('utf-8')
    if not text: return []
    candidates = ([first]+segment(rem) for first,rem in splits(text))
    return max(candidates, key=Pwords)

def splits(text, L=20):
    "Return a list of all possible (first, rem) pairs, len(first)<=L."
    return [(text[:i+1], text[i+1:]) 
            for i in range(min(len(text), L))]

def Pwords(words): 
    "The Naive Bayes probability of a sequence of words."
    return product(Pw(w) for w in words)

#### Support functions 

def product(nums):
    "Return the product of a sequence of numbers."
    return reduce(operator.mul, nums, 1)

class Pdist(dict):
    "A probability distribution estimated from counts in datafile."
    def __init__(self, data=[], N=None, missingfn=None):
        for key,count in data:
	    #print key," +++++++ ",count
	    #try:
		#int(count)
		#key=key.decode('utf-8')
                self[key] = self.get(key,0) + int(count)
		#print "OK"
	    #except:
	        #print "Exception"
	        #if(int(count))

        self.N = float(N or sum(self.itervalues()))
        self.missingfn = missingfn or (lambda k, N: 1./N)
    def __call__(self, key): 
        if key in self: return self[key]/self.N  
        else: return self.missingfn(key, self.N)

def datafile(name, sep=' '):
    "Read key,value pairs from file."
    for line in file(name):
	x,y=line.split(sep)
	x=x.decode('utf-8')        
	yield [x,y]

def avoid_long_words(key, N):
    "Estimate the probability of an unknown word."
    return 10./(N * 10**len(key))

N = 1000000 ## Number of tokens

Pw  = Pdist(datafile('wordlist_filtered.pun'), N, avoid_long_words)

s=[]
with open ("mytest.txt", "r") as myfile:
	for line in myfile:
		s.append(line[:-1]);
#s=s.decode('utf-8')
#### segment2: second version, with bigram counts, (p. 226-227)
os.remove('compare.tsv')
f = open('compare.tsv', 'w')
for i in range(len(s)):
	si=s[i].decode('utf-8')
	for word in segment(si.replace(' ','')):
		f.write(word.encode('utf-8'))
		f.write(' ')
	f.write('\t')
	f.write(si.encode('utf-8'))
	f.write("\n")
