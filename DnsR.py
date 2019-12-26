import os
import sys
import pydig
import argparse
import tldextract
from colorama import *
from multiprocessing import Pool, cpu_count

def attack(sub):

	querys = pydig.query(str(sub),'A' and "CNAME")

	if len(querys) > 0:
		if args["blacklist"]:
			total = 0

			if args["blacklist"].count(",") > 0:
				parse = args["blacklist"].split(",")

				for black in parse:
					for zor in querys:
						if black in zor:
							total += 1
						else:
							pass
			else:
				for zor in querys:
					if args["blacklist"] in zor:
						total += 1
					else:
						pass

			if total == 0:
				if args["output"]:
					PrintNow(sub)
				print(sub)
			else:
				pass
		else:
			if args["output"]:
				PrintNow(sub)
			print(sub)
	else:
		pass



def PrintNow(sub):
	with open(args["output"],"a+",encoding="utf-8") as file:
		file.write(str(sub)+"\n")



def main():

	SubList = list()
	blacklist = ("<",">",",",".","%","&","_","-","|","*","$","é","^","#","/","~","+","(",")","{","}","[","]",";",":")

	#Subdomain stdin den alıyoruz
	for Subdomain in sys.stdin:
		Subdomain = str(Subdomain.rstrip()).lower()

	#Subdomaini kontrol ediyoruz ve içindeki negatif karakterlere göre filitreliyoruz
		if Subdomain:

			tld = tldextract.extract(Subdomain)
			tld = tld.subdomain

			if len(tld) > 63 and not "." in tld:
				pass

			else:
				if not Subdomain.startswith(blacklist):

					if Subdomain.find("..") == -1 and Subdomain.find("--") == -1 and Subdomain.find("*") == -1\
					and Subdomain.find("?") == -1 and Subdomain.find(":") == -1 and Subdomain.find(";") == -1\
					and Subdomain.find("%") == -1 and Subdomain.find("&") == -1 and Subdomain.find("$") == -1\
					and Subdomain.find("-.") == -1 and Subdomain.find(".-") == -1:

						sayı = 0
						whitelist = ["q","w","e","r","t","y","u","o","p","a","s","d","f","g","h","j","k","l","i",
						"z","x","c","v","b","n","m","0","1","2","3","4","5","6","7","8","9",".","_","-"]

						for whitekey in Subdomain:
							if not str(whitekey) in whitelist:
								sayı += 1
							else:
								pass
						if sayı == 0:
							SubList.append(Subdomain)
						else:
							pass

					else:
						pass
				else:
					pass
		else:
			pass

	with Pool(cpu_count()) as p:
		p.map(attack,SubList)

if __name__ == "__main__":

	if os.name == "nt":
		init(convert=True)

	banner = Fore.CYAN+r"""
	 _______                       _______
	|       \                     |       \
	| $$$$$$$\ _______    _______ | $$$$$$$\
	| $$  | $$|       \  /       \| $$__| $$
	| $$  | $$| $$$$$$$\|  $$$$$$$| $$    $$
	| $$  | $$| $$  | $$ \$$    \ | $$$$$$$\
	| $$__/ $$| $$  | $$ _\$$$$$$\| $$  | $$
	| $$    $$| $$  | $$|       $$| $$  | $$
	 \$$$$$$$  \$$   \$$ \$$$$$$$  \$$   \$$
                                        """
	print(banner)
	ap = argparse.ArgumentParser()
	ap.add_argument("-b","--blacklist",required=False,metavar="",help="Delete wildcard Cname or A records")
	ap.add_argument("-o","--output",required=False,metavar="",help="Save output")
	args = vars(ap.parse_args())
	main()
