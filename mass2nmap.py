import sys


#masscan -p1-65535,U:1-65535 10.10.10.x --rate=1000 -e tun0 > ports
#ports=$(python3 cut.py ports)
#nmap -sC -sV -p$ports 10.10.10.x


with open(sys.argv[1], 'r') as my_file:
    ports = my_file.readlines()

p = []

for port in ports:

	x = port.split()[3]
	x = x.replace("/tcp","")
	
	p.append(x)

length = len(p)

i = 0


for port in p:


	if i < length-1:

		prt = (port+",")
		print(prt, end = "")
		i = i+1

	else:
		print(port)

 
