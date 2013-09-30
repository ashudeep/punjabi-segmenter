from sets import Set
import time as time
start_time = time.time()
with open ("mytest.txt", "r") as myfile:
	list_of_words=myfile.read().replace('.',' ').replace('\n',' ').replace('  ',' ').split(' ')
	#print Set(list_of_words)
	bigram_list=[]
	bigram_freqs=[]
	for i in range(len(list_of_words)-1):
		bi=list_of_words[i]+" "+list_of_words[i+1]
		if (bi in bigram_list):
			bigram_freqs[bigram_list.index(bi)]+=1
		else:
			bigram_list.append(bi)
			bigram_freqs.append(1)
	for i in range(len(bigram_list)):
		print bigram_list[i],"\t",bigram_freqs[i]
print "Completed in ",time.time() - start_time, "seconds"
