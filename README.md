# DNS Enumeration Tool

## 📝 Description
This Python tool is designed for DNS enumeration, providing insights into a target domain. It conducts various DNS queries to gather details such as IP addresses, MX records, and NS records. Additionally, it offers the option for subdomain brute-force using a wordlist.

## 🚀 Features
- **Scan Domain:** Retrieve information about the main domain, including IP addresses, MX records, and NS records.
- **Subdomain Brute-Force:** Perform brute-force subdomain enumeration using a wordlist.
- **Generate Report:** Create a detailed report with the gathered information and subdomains found.

## ⚙️ Usage
1. Enter the target domain when prompted.
2. Review the information about the main domain.
3. Optionally, perform subdomain brute-force by providing a wordlist.
4. Review the brute-force results and choose to generate a report.

## 🛠️ Requirements
- Python 3
- `dnspython` library (install via `pip install dnspython`)

## 📋 Instructions
1. Run the script.
2. Enter the target domain.
3. Review the results and follow the prompts for subdomain brute-force and report generation.

## 🌐 Example
```bash
python dns_scanner.py
