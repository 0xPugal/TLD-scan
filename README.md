# TLD-scan
TLD-scan is a Python script designed to scan top-level domains (TLDs) for a given domain. It allows users to specify a domain and a list of TLDs to check if they are available.

## Features
- **Domain Scanning:** Check multiple TLDs for a given domain.
- **Custom Output File:** Specify a custom output file or use the default.
- **Concurrent Processing:** Utilizes threading to speed up domain checking.

## Installation
Clone this repository to your local machine:
```bash
git clone https://github.com/0xPugal/TLD-scan.git
cd TLD-scan
pip install colorama
```

### Help Menu
```
Usage: tld-scan.py [-h] -d DOMAIN -w WORDLIST [-o OUTPUT]

Options:
  -h, --help                show this help message and exit
  -d, --domain DOMAIN       Domain to find TLDs
  -w, --wordlist WORDLIST   JSON file containing list of TLDs
  -o, --output OUTPUT       Output file to save the results (default: {domain}.txt)
```

## Usage
```bash
python3 tld-scan.py -d google -w tld.json
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.