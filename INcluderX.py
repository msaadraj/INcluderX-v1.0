#!/usr/bin/env python3

import argparse
from Core.LFI import lfi_scanner
from Core.RFI import test_rfi
from Validation.Url_Validation import url_validation

def parse_arguments():
    print("")

    parser = argparse.ArgumentParser(usage="INcluderX.py [-h] -u URL [-w WORDLIST] {lfi,rfi} ...",description="IncluderX - Advanced RFI/LFI Vulnerability Scanner", epilog=" ")
    subparsers = parser.add_subparsers(dest="mode",help="Available scan modes",required=True)
    parser.add_argument("-v", "--version", action="version", version="IncluderX v1.0")

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("-w", "--wordlist",help="Payload wordlist file")

    lfi = subparsers.add_parser("lfi",parents=[common_parser],help="Scan for Local File Inclusion")
    lfi.add_argument("-u", "--url", required=True,help="Target URL (example: http://victim.com/index.php?page=)")
    


    rfi = subparsers.add_parser("rfi",parents=[common_parser],help="Scan for Remote File Inclusion")
    rfi.add_argument("-u", "--url", required=True,help="Target URL (example: http://victim.com/index.php?file=)")
    rfi.add_argument("-s", "--server", required=True,help="Hosting server (example: http://attacker.com)")
    rfi.add_argument("-f", "--file", required=True,help="Remote file name (example: shell.txt)")

    return parser.parse_args()


if __name__ == "__main__":
    print("\n\033[91m██╗███╗   ██╗ ██████╗██╗     ██╗   ██╗██████╗ ███████╗██████╗ ██╗  ██╗\033[0m")
    print("\033[92m██║████╗  ██║██╔════╝██║     ██║   ██║██╔══██╗██╔════╝██╔══██╗╚██╗██╔╝\033[0m")
    print("\033[93m██║██╔██╗ ██║██║     ██║     ██║   ██║██║  ██║█████╗  ██████╔╝ ╚███╔╝\033[0m")
    print("\033[94m██║██║╚██╗██║██║     ██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗ ██╔██╗\033[0m")
    print("\033[95m██║██║ ╚████║╚██████╗███████╗╚██████╔╝██████╔╝███████╗██║  ██║██╔╝ ██╗\033[0m")
    print("\033[96m╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝\033[0m v1.0")
    print("\n>>>>>>>>>>>>>>>>>>>>>>> MUHAMMAD SAAD RAJPUT <<<<<<<<<<<<<<<<<<<<<<<<<")
    try:
        args = parse_arguments()
        if args.mode == "lfi":
            lfi_scanner(args.url, args.wordlist, threads=50, timeout=5)

        elif args.mode == "rfi":
            test_rfi(args.url, args.server, args.file)
    except:
        exit(0)
