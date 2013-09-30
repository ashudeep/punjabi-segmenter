#!/usr/bin/python 
# -*- coding: UTF-8 -*-

import sys
i=0;
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
	#print minimum,tot,w,f
def memo(f):
    table = {}
    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]
    fmemo.memo = table
    return fmemo
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
		return 1./tot**7

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
