#!/usr/bin/python
url_stat={}
time_stat={}
with open('access_20170221.log') as f:
	for i in f:
		line=i.split()
		time=float(line[len(line)-1][1:-1])
		url=line[8].split('?')[0]
		if time > 0.1:
			try:
				url_stat[url]+=1
			except:
				url_stat[url]=1
	
			try:
				time_stat[url]+=time
			except:
				time_stat[url]=time
for i in url_stat:
	print('%d\t%.3f\t%s'%(url_stat[i],time_stat[i]/url_stat[i],i))
