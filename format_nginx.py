#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re,sys
import argparse

class nginxLogFormat():
	def __init__(self):
		self.compile = r'(\S+) (\S+) (\S+) (\S+) (\S+)'
		self.args = ''
		self.NF = None

	def set_compile(self, regex, split=' '):
		'''
			q:  匹配双引号里面的内容
			b:  匹配方括号里面的内容
			i:  匹配ip列表，以逗号分隔
			o:  匹配不存在空格的字符串
		'''
		for i in regex:
			if not i in 'oqbi':
				return None
		comp_dict = {'q': r'"([^\"]+)"', 'b': r'\[([^\]]+)\]', 'o': r'(\S+)', 'i': r'([0-9., ]+(?= ))'}
		self.compile = split.join(map(lambda x:comp_dict[x], list(regex)))

	def format_normal(self,string):
		pattern_nginx = re.compile(self.compile)
		match = pattern_nginx.findall(string)
		if self.NF == None:
			return match[0]
		else:
			return map(lambda x:match[0][int(x)],self.NF)


	def set_NF(self,NF):
		self.NF = NF.split(',')

	def format(self, string):
		pattern_nginx = re.compile(r'(\S+) "([^\"]+)" (\S+) (\S+) (\[[^\]]+\]) ("[^\"]+") (\d+) (\d+) (\S+) ("[^\"]+") (\S+)')
		pattern_path = re.compile(r'/[^? ]*')
		match = pattern_nginx.findall(string)
		client_ip = match[0][1].split(',')[0]
		path = pattern_path.search(match[0][5]).group()
		status_code, delay = match[0][6], match[0][10]
		return client_ip, status_code, path, delay

	def fromFile(self, filename):
		#try:
		with open(filename) as f:
			for line in f:
				yield self.format_normal(line)
		#except:
		#	yield None

	def formStdin(self):
		for line in sys.stdin:
			yield self.format_normal(line)

	def facFormat(self):
		self.parse_args()
		if self.isfile():
			filename = self.args.filename
			return self.fromFile(filename)
		else:
			return self.formStdin()

	def isfile(self):
		if len(sys.argv)%2 ==0:
			return True
		else:
			return False
	def parse_args(self):
		description = '''
				author: xiaofengfeng
		'''
		parser = argparse.ArgumentParser(description=description)
		help = '设置正则表达式变量,q:  匹配双引号里面的内容,b:  匹配方括号里面的内容,i:  匹配ip列表，以逗号分隔,o:  匹配不存在空格的字符串'
		parser.add_argument("-c","--compile",dest="compile",type=self.set_compile,help=help)
		help = '设置输入哪些列，例如：‘1，2，3，4’表示输出1，2，3，4列'
		parser.add_argument("-n","--nf", dest="NF", type=self.set_NF,help=help)
		if self.isfile():
			help = 'filename'
			parser.add_argument("filename",help=help)
		self.args  = parser.parse_args()

if __name__ == '__main__':
	f = nginxLogFormat()
	#f.set_compile('ioobqooqqqq')
	for i in f.facFormat():
		print i


#./format_nginx.py -c ioobqooqqqq -n '5,6,7'   filename
#tail -f filename | ./format_nginx.py -c ioobqooqqqq -n '5,6,7'
#要nginx用awk分成一列一列的还是有困难的。所以写了一个脚本用来分割nginx日志，-c 后面是跟代码内定义的正则表达式块。如果不够用的可以扩充。-n 表示你要输出那几列