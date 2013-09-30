i=0;
with open ("wordlist_full_mod2.pun", "r") as myfile:
	for line in myfile:			
		line=line
		try:
			[f,w]=line.split(' ');
			w=w[:-1]	
		except ValueError:
			continue
		if(int(f)>=2):
			print w,f
