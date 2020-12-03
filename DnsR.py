import re
import os
import sys
import argparse
import threading
import tldextract
import dns.resolver
import urllib.parse
from colorama import *
from concurrent.futures import ThreadPoolExecutor

class DnsResolver():

    def __init__(self):

        init(autoreset=True)
        self.target_list = list()
        self.print_lock = threading.Lock()

        if args.stdin and not args.list:

            [self.target_list.append(str(x)) for x in urllib.parse.unquote(sys.stdin.read()).replace("*.","").split("\n") if x and not self.control(x) and self.control_two(x)]

            if not self.target_list:

                print(Fore.RED+"Subdomains Not Found In Stdin")

                sys.exit()

        elif args.list and not args.stdin:

            if not os.path.exists(args.list):

                print(Fore.RED+"File Not Found:",args.list)

                sys.exit()

            with open(args.list, "r", encoding="utf-8") as f:

                [self.target_list.append(x) for x in urllib.parse.unquote(f.read()).replace("*.","").split("\n") if x and not self.control(x) and self.control_two(x)]

                if not self.target_list:

                    print(Fore.RED+"Your Subdomain List IS Empty:",args.list)

        else:

            print(Fore.RED+"""

            \rYou Used The Wrong Parameter""",Fore.MAGENTA+"""


            \rUsage:
            \r------

            \rpython3 DnsR.py --list subdomains.txt --output resolved.txt

            \rcat subdomains.txt | python3 DnsR.py --stdin --output resolved.txt

            \rpython3 DnsR.py --list subdomains.txt --blacklist 198.55.44.77

            \rcat subdomains.txt | python3 DnsR.py --stdin --blacklist 198.55.44.77

            \rpython3 DnsR.py --list subdomains.txt --thread 50 --blacklist 198.55.44.77,xx.example.com

            \rcat subdomains.txt | python3 DnsR.py --stdin --blacklist 198.55.44.77,xx.example.com

            """)

            sys.exit()

        resolvers_ips = ['1.1.1.1','1.0.0.1','8.8.8.8','8.8.4.4','77.88.8.8','77.88.8.1']

        self.Dnspython_Resolver = dns.resolver.Resolver()
        self.Dnspython_Resolver.timeout = 7
        self.Dnspython_Resolver.nameservers = resolvers_ips

        if args.blacklist:

            if not "," in args.blacklist:

                x = ".*" + str(args.blacklist).replace(".",r"\.") + "*."
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


        with ThreadPoolExecutor(max_workers=args.thread) as executor:

            executor.map(self.resolve_subs, self.target_list)


    def resolve_subs(self, target):

        try:

            dns_query = self.Dnspython_Resolver.resolve(target, "A")

            ip_address = dns_query[0].to_text()

            cname = dns_query.canonical_name.to_text()

            if self.analysist([ip_address, cname]):

                self.print_now(target)

        except dns.resolver.NXDOMAIN as nx:

            cname = nx.canonical_name.to_text()

            if cname.endswith("."):

                cname = cname[:-1]

            if target != cname:

                if self.analysist([cname]):

                    self.print_now(target)

        except:
            pass

    def analysist(self, results):

        if args.blacklist:

            filter_blacklist = list(filter(self.BlackList.match, results))

            if not filter_blacklist:

                return True

            else:

                return False

        else:

            return True

    def print_now(self, target):

        with self.print_lock:

            print(Fore.GREEN+str(target))


        if args.output:

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

            pass

    def control_two(self,subdomain):

        try:
            if subdomain.endswith(".") or subdomain.endswith("-") or subdomain.endswith("_") or subdomain.startswith(".") or subdomain.startswith("-"):
                return False
            else:
                return True
        except:
            pass

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-l", "--list", metavar="", required=False, help="Targets List")
    ap.add_argument("-s", "--stdin", action="store_true", required=False, help="Read Subdomains From Stdin")
    ap.add_argument("-b", "--blacklist", metavar="", required=False, help="Filter Blacklist")
    ap.add_argument("-o", "--output", metavar="", required=False, help="Save Output")
    ap.add_argument("-t", "--thread", metavar="", default=20, type=int, required=False, help="Thread Number(Default-20)")
    args = ap.parse_args()

    Start_attack = DnsResolver()
