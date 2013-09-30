i=0;
words=[]
freqs=[]
with open ("english_us_wordlist_full.txt", "r") as myfile:
	for line in myfile:			
		[w,f]=line.split('\t');	
		words.append(w);
		freqs.append(int(f));
		tot=float(sum(freqs));
		for i in range(len(freqs)):
			freqs[i]=freqs[i]/tot;
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
	

def Pw(w):
	return int(freqs[words.index(w)])
print segment("myname");

