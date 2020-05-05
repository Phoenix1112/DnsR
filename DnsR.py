import re
import os
import sys
import pydig
import argparse
import threading
import tldextract
import urllib.parse
from colorama import *
from concurrent.futures import ThreadPoolExecutor

class DnsR():

	def __init__(self):


		init(autoreset=True)
		self.target_list = list()
		self.lock = threading.Lock()
		self.domain_list = list()


		if args.stdin and not args.list:

			[self.target_list.append(str(x)) for x in urllib.parse.unquote(sys.stdin.read()).replace("*.","").split("\n") if x and not self.control(x)]

			if not self.target_list:

				print(Fore.RED+"Subdomains Not Found In Stdin")

				sys.exit()


		elif args.list and not args.stdin:

			if not os.path.exists(args.list):

				print(Fore.RED+"File Not Found:",args.list)

				sys.exit()


			with open(args.list, "r", encoding="utf-8") as f:

				[self.target_list.append(x) for x in urllib.parse.unquote(f.read()).replace("*.","").split("\n") if x and not self.control(x)]


		else:

			print(Fore.RED+"""

			\rYou Used The Wrong Parameter""",Fore.MAGENTA+"""


			\rUsage:
			\r------

			\rpython3 DnsR.py --list subdomains.txt --output resolved.txt

			\rcat subdomains.txt | python3 DnsR.py --stdin --output resolved.txt

			\rpython3 DnsR.py --list subdomains.txt --blacklist 198,55,44,77

			\rcat subdomains.txt | python3 DnsR.py --stdin --blacklist 198,55,44,77

			\rpython3 DnsR.py --list subdomains.txt --thread 50 --blacklist 198,55,44,77,xx.example.com

			\rcat subdomains.txt | python3 DnsR.py --stdin --blacklist 198,55,44,77,xx.example.com

			""")

			sys.exit()


		self.resolver = pydig.Resolver(nameservers=[
			'1.1.1.1','1.0.0.1',
			'8.8.8.8','8.8.4.4',
			'77.88.8.8','77.88.8.1',
			'64.6.64.6','64.6.65.6',
			'8.26.56.26','8.20.247.20',
			'9.9.9.9','149.112.112.112',
			'185.228.168.9','185.228.169.9',
			'198.101.242.72','23.253.163.53',
			'208.67.222.222','208.67.220.220',
			'176.103.130.130','176.103.130.131'])


		if args.blacklist:

			if not "," in args.blacklist:

				x = args.blacklist

				x = ".*" + x.replace(".",r"\.") + "*."

				self.BlackList = re.compile(x)

			else:

				x = args.blacklist.split(",")

				y = []

				for i in x:

					if i:

						i = ".*" + i.replace(".", r"\.") + "*."

						y.append(i)

				req = ("|").join(y)

				self.BlackList = re.compile(req)


		self.target_list = list(set(self.target_list))


		with ThreadPoolExecutor(max_workers=args.thread) as executor:

			for x in self.target_list:
				
				if x.startswith(".") or x.startswith("-"):
					x = x[1:]

				executor.submit(self.resolve_subs, x)


	def resolve_subs(self,target):

		try:

			dns_query = self.resolver.query(target, 'A')

			if dns_query:

				if not args.blacklist:

					with self.lock:

						print(Fore.GREEN+str(target))

					if args.output:

						self.save_output(target)

				else:

					find_blacklist = list(filter(self.BlackList.match, dns_query))

					if not find_blacklist:

						with self.lock:

							print(Fore.GREEN+str(target))

						if args.output:

							self.save_output(target)
			else:

				pass

		except:
			pass



	def save_output(self,target):

		with open(args.output, "a+", encoding="utf-8") as f:

			f.write(str(target) + "\n")



	def control(self,subdomain):

		try:

			regex = re.findall(r"é|!|'|\^|\+|\$|%|\*|/|\.\-|\-\.|\?|&|#",str(subdomain))

			if regex:

				return True

			else:

				return False

		except:

			return False


if __name__ == "__main__":

	ap = argparse.ArgumentParser()
	ap.add_argument("-l", "--list", metavar="", required=False, help="Targets List")
	ap.add_argument("-s", "--stdin", action="store_true", required=False, help="Read Subdomains From Stdin")
	ap.add_argument("-b", "--blacklist", metavar="", required=False, help="Filter Blacklist")
	ap.add_argument("-o", "--output", metavar="", required=False, help="Save Output")
	ap.add_argument("-t", "--thread", metavar="", default=20, type=int, required=False, help="Thread Number(Default-20)")
	args = ap.parse_args()

	Run = DnsR()
