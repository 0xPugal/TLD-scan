import argparse
import json
import socket
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

VERSION = "v0.1"
init()

def print_banner():
    banner_text = r"""
{}╔╦╗╦  ╔╦╗┌─┐┌─┐┌─┐┌┐┌
 ║ ║   ║║└─┐│  ├─┤│││
 ╩ ╩═╝═╩╝└─┘└─┘┴ ┴┘└┘ @0xPugal{}""".format(Fore.WHITE + Style.BRIGHT, Style.RESET_ALL)
    print(banner_text)

def print_description():
    description_text = "Top Level Domain Scanner"
    print(f"{Fore.WHITE + Style.BRIGHT}{description_text}{Style.RESET_ALL}")
    print("")

def print_help():
    print_banner()
    print_description()
    print("Usage: tld-scan.py [-h] -d DOMAIN -w WORDLIST [-o OUTPUT]")
    print("")
    print("Options:")
    print(f"  -h, --help            show this help message and exit")
    print(f"  -d DOMAIN, --domain DOMAIN")
    print(f"                        Domain to find TLDs")
    print(f"  -w WORDLIST, --wordlist WORDLIST")
    print(f"                        JSON file containing list of TLDs")
    print(f"  -o OUTPUT, --output OUTPUT")
    print(f"                        Output file to save the results (default: {{domain}}.txt)")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Top Level Domain Scanner by @0xPugal",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-d', '--domain', required=False, help='Domain to find TLDs')
    parser.add_argument('-w', '--wordlist', required=False, help='JSON file containing list of TLDs')
    parser.add_argument('-o', '--output', help='Output file to save the results (default: {domain}.txt)')
    return parser

def load_tld_list(file_names):
    tlds = []
    for file_name in file_names:
        with open(file_name, 'r') as file:
            tlds.extend(json.load(file))
    return tlds

def check_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False

def log_found(domain, output_file):
    print(f"{Fore.GREEN + Style.BRIGHT}[FOUND]{Style.RESET_ALL} {domain}")
    with open(output_file, 'a') as file:
        file.write(domain + '\n')

def main():
    parser = parse_arguments()
    args = parser.parse_args()
    domain = args.domain
    file_names = args.wordlist.split(',') if args.wordlist else []
    
    if not domain or not file_names:
        print(f"{Fore.RED + Style.BRIGHT}Domain and TLD list are required.{Style.RESET_ALL}")
        sys.exit(1)

    output_file = args.output if args.output else f"{domain}.txt"

    tlds = load_tld_list(file_names)
    total_tlds = len(tlds)

    print_banner()
    print_description()
    print(" ")
    print("-----------------------------------------------------")
    print(f"{Fore.CYAN + Style.BRIGHT}Total TLDs to scan: {total_tlds}{Style.RESET_ALL}")
    print("-----------------------------------------------------")

    start_time = time.time()
    found_count = 0

    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_domain = {executor.submit(check_domain, f"{domain}.{tld}"): tld for tld in tlds}
        for future in future_to_domain:
            tld = future_to_domain[future]
            try:
                if future.result():
                    found_count += 1
                    log_found(f"{domain}.{tld}", output_file)
            except Exception as exc:
                print(f"{Fore.WHITE + Style.BRIGHT}{domain}.{tld} generated an exception: {exc}{Style.RESET_ALL}")

    elapsed_time = time.time() - start_time
    output_file_path = os.path.abspath(output_file)

    result = f"Scan finished, scanner took {elapsed_time:.2f} seconds, found {found_count} domains, output saved to {output_file_path}\n"
    print(f"{Fore.WHITE + Style.BRIGHT}{result}{Style.RESET_ALL}")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # Do nothing if no arguments are provided
        pass
    elif '--help' in sys.argv or '-h' in sys.argv:
        print_help()
    else:
        main()
