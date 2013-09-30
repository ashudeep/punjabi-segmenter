# -*- coding: utf-8 -*-
import re, string, random, glob, operator, heapq, os
from collections import defaultdict
from math import log10
from prec_rec_f_2 import *

def memo(f):
    "Memoize function f."
    table = {}
    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]
    fmemo.memo = table
    return fmemo

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


def product(nums):
    "Return the product of a sequence of numbers."
    return reduce(operator.mul, nums, 1)

class Pdist(dict):
    "A probability distribution estimated from counts in datafile."
    def __init__(self, data=[], N=None, missingfn=None):
        for key,count in data:
                self[key] = self.get(key,0) + int(count)

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

def datafile2(name, sep='\t'):
    "Read key,value pairs from file."
    for line in file(name):
        x,y,z=line.split(sep)
        x=x.decode('utf-8')        
        y=y.decode('utf-8')
        yield [x+" "+y,z]

def avoid_long_words(key, N):
    "Estimate the probability of an unknown word."
    return 10./((N) * 10**len(key))

N = 1000000 ## Number of tokens

Pw  = Pdist(datafile('wordlist_filtered.pun'), N, avoid_long_words)

def cPw(word, prev):
    "Conditional probability of word, given previous word."
    try:
        return P2w[prev + ' ' + word]/float(Pw[prev])
    except KeyError:
        return Pw(word)

P2w = Pdist(datafile2('Pan_2-Grams.txt'), N)

@memo 
def segment2(text, prev='<S>'): 
    "Return (log P(words), words), where words is the best segmentation." 
    if not text: return 0.0, [] 
    candidates = [combine(log10(cPw(first, prev)), first, segment2(rem, first)) 
                  for first,rem in splits(text)] 
    return max(candidates) 

def combine(Pfirst, first, (Prem, rem)): 
    "Combine first and rem results into one (probability, words) pair." 
    return Pfirst+Prem, [first]+rem 



s=[]
with open ("mytest.txt", "r") as myfile:
	for line in myfile:
		s.append(line[:-1]);
#s=s.decode('utf-8')

os.remove('compare2.tsv')
f = open('compare2.tsv', 'w')
for i in range(len(s)):
	si=s[i].decode('utf-8')
	for word in segment2(si.replace(' ',''))[1]:
		f.write(word.encode('utf-8'))
		f.write(' ')
	f.write('\t')
	f.write(si.encode('utf-8'))
	f.write("\n")
print "Results using Bigram data"
#precision_recall_f("compare2.tsv")
i=0
f="compare2.tsv"
big_list1=[]
big_list2=[]
with open(f,'r') as f:
	for line in f:
		[line1,line2]=line.split('\t');
		line2=line2#[:-1]#remove the newline character
		#print line1,line2
		if(len(get_binary_list(line1))!=len(get_binary_list(line2))):
			continue
		else:
			i=i+1
			big_list1.extend(get_binary_list(line1));
			big_list2.extend(get_binary_list(line2));
	#print i
	#print big_list1,big_list2
	#print len(big_list1),len(big_list2)
	prec=precision(big_list1,big_list2)
	rec=recall(big_list1,big_list2)
	print "precision=",prec,"recall=",rec,"fscore=",fscore(prec,rec);

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
#precision_recall_f('compare.tsv')
print "Results using Unigram data"
i=0
f="compare.tsv"
big_list1=[]
big_list2=[]
with open(f,'r') as f:
	for line in f:
		[line1,line2]=line.split('\t');
		line2=line2#[:-1]#remove the newline character
		#print line1,line2
		if(len(get_binary_list(line1))!=len(get_binary_list(line2))):
			continue
		else:
			i=i+1
			big_list1.extend(get_binary_list(line1));
			big_list2.extend(get_binary_list(line2));
	#print i
	##print big_list1,big_list2
	#print len(big_list1),len(big_list2)
	prec=precision(big_list1,big_list2)
	rec=recall(big_list1,big_list2)
	print "precision=",prec,"recall=",rec,"fscore=",fscore(prec,rec);


