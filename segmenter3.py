#!/usr/bin/python 
# -*- coding: UTF-8 -*-
import sys
from math import log10
i=0;
def memo(f):
    table = {}
    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]
    fmemo.memo = table
    return fmemo

words=[]
freqs=[]
with open ("wordlist_filtered.pun", "r") as myfile:
	for line in myfile:	
		try:		
			[w,f]=line.split(' ');	
			w=w.decode('utf-8')
		except ValueError:
			continue
		words.append(w);
		freqs.append(int(f));
	tot=float(sum(freqs));
	minimum=min(freqs);

bi_w=[]
freqs_bi=[]
with open ("Pan_2-Grams.txt", "r") as myfile:
	for line in myfile:	
		try:		
			[w1,w2,f]=line.split('\t');	
			w1=w1.decode('utf-8')
			w2=w2.decode('utf-8')
			f=int(f)
			bi_w.append(w1+' '+w2);
			freqs_bi.append(f);
		except ValueError:
			continue
tot_bi=float(sum(freqs_bi))
minimum=min(freqs_bi)

def cPw(word, prev):
    "Conditional probability of word, given previous word."
    try:
    	#print "try"
        return freqs_bi[bi_w.index(prev+' '+word)]/(float(tot_bi)*float(Pw(prev)))
    except KeyError:
        #print "except"
        return Pw(word)
    except ValueError:
    	return Pw(word)    


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


@memo
def segment(text):
	#text=text
	#"Return a list of words that is the best segmentation of text."
	if not text: return []
	candidates = ([first]+segment(rem) for first,rem in splits(text))
	return max(candidates, key=Pwords)
def splits(text, L=20):
	#"Return a list of all possible (first, rem) pairs, len(first)<=L."
	return [(text[:i+1], text[i+1:])
 		for i in range(min(len(text), L))]
def Pwords(words):
	#"The Naive Bayes probability of a sequence of words."
	prod=1.0
	for w in words:
		prod*=Pw(w)
	return prod
	
tot4=pow(tot,4)
def Pw(w):
	try:
		return freqs[words.index(w)]/tot
	except ValueError:
		return 1/tot**5
s=[]
with open ("mytest.txt", "r") as myfile:
	for line in myfile:
		s.append(line[:-1]);			

#print isinstance(s,unicode)
for i in range(len(s)):
	si=s[i].decode('utf-8')
	for word in segment(si.replace(' ','')):
		sys.stdout.write(word.encode('utf-8'))
		sys.stdout.write(' ')
	sys.stdout.write('\t')
	print si.encode('utf-8')
	
#print repr(segment(s)).decode("utf-8")
