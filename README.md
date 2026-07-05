# Subdomain enumeration tool for HackerOne

This tool is for enumerating live and inscope subdomains on HackerOne bug bounties.
(not perfect yet, especially the out of scope flags)

To use the tool you must download the csv scope for the program your hacking on and it will remove all out of scope items from your subdomains list.

### Installation and usage
- `git clone https://github.com/gilbertormail-collab/Subdomain-enum-tool`
- `cd Enumerator`
- `python3 enumerator.py -u example.com -csv path_to_csv_scope -endpoints`