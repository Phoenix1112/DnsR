import os
import sys
import pydig
import argparse
import threading
from colorama import *
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

def attack(sub):

    try:

        query_A = pydig.query(sub, "A")

        if query_A:

            if args.output:
                save_output(sub)

            with print_lock:
                print(Fore.GREEN+sub)

        else:

            query_cname = pydig.query(sub, "CNAME")

            if query_cname:

                if args.output:
                    save_output(sub)

                with print_lock:
                    print(Fore.GREEN+sub)

    except:
        pass

def save_output(x):

    with open(args.output, "a+", encoding="utf-8") as f:
        f.write(str(x) + "\n")


def main():

    target_list = list()

    if args.list:

        if not os.path.exists(args.list):
            print(Fore.RED+"Target List Not Found: {}".format(args.list))
            sys.exit()

        print(banner)

        with open(args.list, "r", encoding="utf-8") as f:
            [target_list.append(x) for x in f.read().lower().split("\n") if x and black_character(x)]

    elif args.stdin:

        [target_list.append(x) for x in sys.stdin.read().lower().split("\n") if x and black_character(x)]

    else:

        print(Fore+RED+"You Need To Use --list Or --stdin Param")
        sys.exit()


    if target_list:

        with ThreadPoolExecutor(max_workers=args.thread) as executor:
            for sub in target_list:
                executor.submit(attack, sub)

    else:

        print(Fore.RED+"Not Found Any Target")
        sys.exit()

def black_character(subdomain):

    try:

        character_list = [".-", "-.", "&", "%", "(", ")", "$", "#", "<", ">", "/", "*",
        "?", "~", ",", ";", ":", "|", "{", "}", "[","]", "^", "'", "+"]

        sayı = 0

        for black in character_list:

            if black in subdomain:

                sayı += 1
                break

            else:
                pass

        if sayı == 0:

            return True

        else:

            return False

    except:

        return False



if __name__ == "__main__":

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

    ap = argparse.ArgumentParser()
    ap.add_argument("-l","--list", required=False, metavar="", help="Read Targets From List")
    ap.add_argument("-s","--stdin", required=False, action="store_true", help="Read Targets From Stding")
    ap.add_argument("-o","--output", required=False, metavar="", help="Save output")
    ap.add_argument("-t", "--thread", required=False, metavar="",default=20, type=int, help="Thread Number(Default-20)")
    args = ap.parse_args()

    print_lock = threading.Lock()

    main()
