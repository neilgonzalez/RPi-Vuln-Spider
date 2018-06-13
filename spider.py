#simple python network spider for raspberry pi or other linux pentsting
#requires nikto and nmap

import subprocess
import re
import sys
import getopt

def menu():
	print "usage: python spider.py <options>"
	print "options:"
	print "-n number of endpoints to scan (default 24)"
	print "-l [filename.txt] logs output to specified file name"

def is_num(s):
    return any(i.isdigit() for i in s)

def main(argv):
	opts, args = getopt.getopt(argv,"hn:l:",["EPnum=","logs="])
	if opts[0][0] == '-n':
		if int(opts[0][1]) > 0:
			ps = subprocess.Popen(['nmap', '-sn', '192.168.1.1/' + opts[0][1]], stdout=subprocess.PIPE)

	else:
		ps = subprocess.Popen(['nmap', '-sn', '192.168.1.1/24'], stdout=subprocess.PIPE)
	
	output = ps.communicate()[0]
	lst = output.split(" ")
	coll = []
	ip_list = []
	ip_list_CLEAR=[]

	for x in lst:
		if (re.findall(r'\bH\w+', x)):
		
			pos2 = x.find('H')
			prime = x[0:pos2]
			prime = prime.replace('(', '')
			prime = prime.replace(')', '')
			ip_list.append(prime)
	for x in ip_list:
		clear = ""
		for char in x:
			if char != '\n' and  char != ' ':
				clear = clear + char
		ip_list_CLEAR.append(clear)		
	ports = {}

	for ip_counter in range (0, len(ip_list_CLEAR)):
		ports_list =[]
		ps2 = subprocess.Popen(['nmap', '-sT', ip_list_CLEAR[ip_counter]], stdout=subprocess.PIPE)
		output2 = ps2.communicate()[0]
		lst2 = output2.split(" ")

		for x in lst2:
			if(is_num(x)):
				if x.find('/') > 1:
					portsNum = x[0:x.find('/')]
					portsNum_CLEAR = portsNum[x.find('\n')+1:]
					ports_list.append(portsNum_CLEAR)

		ports[ip_list_CLEAR[ip_counter]] = ports_list

	numSize = 0
	for x in ip_list_CLEAR:
		numSize = numSize + len(ports[x])
	for x in ports:
		for y in range(0, len(ports[x])):
			ps3 = subprocess.Popen(['nikto', '-host', x, '-port', str(ports[x][y-1] )], stdout=subprocess.PIPE)
			output3 = ps3.communicate()[0]
			if opts[1][0] == '-l':
				sys.Popen([output3,'>',opts[1][1]])
			else:
				print output3
if __name__ == "__main__":
   main(sys.argv[1:])
