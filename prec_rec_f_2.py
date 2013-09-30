#!/usr/bin/python 
# -*- coding: UTF-8 -*-
def fscore (precision, recall):
	if (precision+recall!=0):
		return 2*precision*recall/(precision+recall)
	else:
		return 0

def precision(list1,list2):#lists should be 1,0 lists and same size
#list 2 is (gold standard) hand tagged list
#list 1 is the code generated list
	main_list=[]
	if len(list1)!=len(list2):
		print "Error! Sizes dont match"
		return -1
	else:
		#print list1,list2
		for i in xrange(len(list1)):
			if (list1[i]==1 and list1[i]==list2[i]):
				main_list.append(1);
			else:
				main_list.append(0);
		#print main_list;
		return float(sum(main_list))/sum(list1)		

def recall(list1, list2):
#lists should be 1,1 and same size
#list 2 is hand tagged list
#list 1 is the code generated list
	main_list=[]	
	if len(list1)!=len(list2):
		print "Error! Sizes dont match"
		return -1
	else:
		for i in xrange(len(list1)):
			if (list1[i]==1 and list1[i]==list2[i]):
				main_list.append(1);
			else:
				main_list.append(0);
		return float(sum(main_list))/sum(list2)

def get_binary_list(line):
	bin_list=[]
	flag=0
	for i in xrange(len(line)):
		if(line[i]==' '):
			bin_list.append(1);
			flag=1;
		else:
			if(flag==1):
				flag=0;
			else:
				bin_list.append(0);
	return bin_list

def compare_lines(line1,line2):
	list1=get_binary_list(line1);
	list2=get_binary_list(line2);
	print precision(list1,list2), recall(list1,list2),fscore(precision(list1,list2), recall(list1,list2));
#list1=[0,1,0,0,0,1,1,0,0];
#list2=[0,0,0,0,1,1,0,0,0];
#line1="Ashu+deep+singh"
#line2="Ashudeep+singh"
#print compare_lines(line1,line2);
'''
def precision_recall_f(fil):
	i=0
	f=fil
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
		print i
		#print big_list1,big_list2
		#print len(big_list1),len(big_list2)
		prec=precision(big_list1,big_list2)
		rec=recall(big_list1,big_list2)
		print "precision=",prec,"recall=",rec,"fscore=",fscore(prec,rec);
'''
