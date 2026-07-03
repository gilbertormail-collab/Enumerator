import csv
import string
import subprocess
from pyfiglet import Figlet
import argparse
import colorama
from urllib.parse import urlparse
import random

def load_out_of_scope_csv(csv_file):
    out_of_scope = set()
    
    with open(csv_file, newline="", encoding="utf8") as file:
        reader = csv.DictReader(file) 
        
        for row in reader:
            identifier = row.get("identifier", "").strip()
            if identifier.startswith("*."):
                identifier = identifier[2:]
            
            if not identifier:
                continue
            
            parsed = urlparse(identifier)
            if parsed.scheme or parsed.path not in ("", "/"):
                print(f"[{colorama.Fore.RED}Out Of Scope{colorama.Style.RESET_ALL}] Endpoint found in csv: {identifier}")
                
            out_of_scope.add(identifier.lower())
            
    return out_of_scope


def filter_out_of_scope(live_file, out_of_scope):
    filtered = []
    
    with open(live_file) as file2:
        for line in file2:
            domain = line.strip().lower()
            
            if not domain:
                continue
            
            blocked = False
            
            for ooscope in out_of_scope:
                if domain == ooscope or domain.endswith("." + ooscope):
                    blocked = True
                    break
            if not blocked:
                filtered.append(domain)
    return filtered
                    


def main():
    fig = Figlet(font="banner")
    print(fig.renderText("Enumerator"))
    print("For HackerOne Bug bounty programs.")
    # make a feature to check for latest releases from git and make an update command
    print("V1.0.0")
    parser = argparse.ArgumentParser(prog="enumerator")
    parser.add_argument("-u", "--url", help="Target URL")
    parser.add_argument("-csv", "--csv", help="The path to your HackerOne bug bounty's csv scope")
    
    args = parser.parse_args()

    if args.url:
        result = subprocess.run(["subfinder", "-d", args.url], capture_output=True, text=True, check=True)
        with open("domains/domains.txt", "w") as f:
            f.write(result.stdout)
        count = len(result.stdout.splitlines())
        print(f"[{colorama.Fore.CYAN}INFO{colorama.Style.RESET_ALL}] Found {count} subdomains.")
        
        live_result = subprocess.run(["httpx", "-l", "domains/domains.txt"], capture_output=True, text=True, check=True)
        with open("domains/live.txt", "w") as f2:
            f2.write(live_result.stdout)
        count2 = len(live_result.stdout.splitlines())
        print(f"[{colorama.Fore.CYAN}INFO{colorama.Style.RESET_ALL}] Found {count2} live subdomains.")
        if args.csv:
            out_of_scope = load_out_of_scope_csv(args.csv)
            filtered = filter_out_of_scope("domains/live.txt",out_of_scope)
            rand_str = "".join(random.choices(string.ascii_lowercase, k=6))
            with open(f"results/{rand_str}.txt", "w") as f3:
                f3.write("\n".join(filtered))
            print(f"[{colorama.Fore.GREEN}DONE{colorama.Style.RESET_ALL}] Saved {len(filtered)} live domains in scope to results/{rand_str}.txt")
            
            
            
if __name__ == "__main__":
    main()