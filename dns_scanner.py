# Nicolas Poersch (@nicolaspoersch)
import dns.resolver
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
import time

# Defina o nome da sua ferramenta
TOOL_NAME = """
  ███████╗███████╗███╗   ██╗██████╗ 
 ██╔════╝██╔════╝████╗  ██║██╔══██╗
 ███████╗█████╗  ██╔██╗ ██║██║  ██║
 ╚════██║██╔══╝  ██║╚██╗██║██║  ██║
 ███████║███████╗██║ ╚████║██████╔╝
 ╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝ 
"""

VERSION_INFO = "Version: v1"
GITHUB_INFO = "GitHub: @nicolaspoersch"

def clear_terminal():
    # Limpar o terminal com base no sistema operacional
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_banner():
    clear_terminal()
    print(TOOL_NAME)
    print(VERSION_INFO)
    print(GITHUB_INFO)

def scan_domain(domain):
    results = {'main_domain': domain, 'ip_addresses': [], 'mx_records': [], 'ns_records': []}

    try:
        answers_a = dns.resolver.resolve(domain, 'A')
        results['ip_addresses'] = [answer.address for answer in answers_a]

        answers_mx = dns.resolver.resolve(domain, 'MX')
        results['mx_records'] = [(rdata.exchange, rdata.preference) for rdata in answers_mx]

        answers_ns = dns.resolver.resolve(domain, 'NS')
        results['ns_records'] = [rdata.target for rdata in answers_ns]

    except dns.resolver.NoAnswer:
        print(f"No answer for {domain}")

    return results

def list_txt_files_in_folder():
    txt_files = [f for f in os.listdir() if f.endswith('.txt')]
    return txt_files

def resolve_subdomain(subdomain, domain):
    full_domain = f"{subdomain}.{domain}"
    start_time = time.time()
    try:
        answers = dns.resolver.resolve(full_domain, 'A')
        end_time = time.time()
        elapsed_time = end_time - start_time
        return full_domain, [answer.address for answer in answers], elapsed_time
    except dns.resolver.NXDOMAIN:
        return None

def brute_force_subdomains(domain, wordlist_file):
    found_subdomains = {}

    with open(wordlist_file, 'r') as file:
        subdomain_list = file.read().splitlines()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(resolve_subdomain, subdomain, domain) for subdomain in subdomain_list]

        for future in futures:
            result = future.result()
            if result:
                subdomain, ip_addresses, elapsed_time = result
                print(f"Subdomain found: {subdomain} (Time: {elapsed_time:.4f} seconds)")

                if ip_addresses:
                    print(f"  IPs: {', '.join(ip_addresses)}")

                found_subdomains[subdomain] = {'ip_addresses': ip_addresses, 'elapsed_time': elapsed_time}

    return found_subdomains

def print_results(results):
    print("\nMain domain:")
    print(f"{results['main_domain']} - {', '.join(results['ip_addresses'])}")

    print("\nMX records:")
    for mx_record in results['mx_records']:
        print(f"{mx_record[0]} - Preference: {mx_record[1]}")

    print("\nNS records:")
    for ns_record in results['ns_records']:
        print(ns_record)

def generate_report(results, found_subdomains):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"report_{results['main_domain']}_{timestamp}.txt"

    with open(report_filename, 'w') as report_file:
        report_file.write(f"DNS Report for the domain {results['main_domain']}\n")
        report_file.write("\nMain domain:\n")
        report_file.write(f"{results['main_domain']} - {', '.join(results['ip_addresses'])}\n")

        report_file.write("\nMX records:\n")
        for mx_record in results['mx_records']:
            report_file.write(f"{mx_record[0]} - Preference: {mx_record[1]}\n")

        report_file.write("\nNS records:\n")
        for ns_record in results['ns_records']:
            report_file.write(f"{ns_record}\n")

        report_file.write("\nFound subdomains:\n")
        for subdomain, info in found_subdomains.items():
            report_file.write(f"{subdomain} - IPs: {', '.join(info['ip_addresses'])} - Time: {info['elapsed_time']:.4f} seconds\n")

    print(f"\nReport generated successfully: {report_filename}")

if __name__ == "__main__":
    print_banner()

    target_domain = input("Enter the target domain: ")

    results = scan_domain(target_domain)

    print("\nMain domain:")
    print(f"{results['main_domain']} - {', '.join(results['ip_addresses'])}")

    print("\nMX records:")
    for mx_record in results['mx_records']:
        print(f"{mx_record[0]} - Preference: {mx_record[1]}")

    print("\nNS records:")
    for ns_record in results['ns_records']:
        print(ns_record)

    brute_force_choice = input("\nDo you want to perform subdomain brute-force? (Y/N): ").strip().lower()

    if brute_force_choice == 'y':
        txt_files_in_folder = list_txt_files_in_folder()

        if txt_files_in_folder:
            print("\n.txt files in the folder:")
            for i, txt_file in enumerate(txt_files_in_folder, start=1):
                print(f"{i} | {txt_file}")
        else:
            print("No .txt files found in the folder.")

        wordlist_index = int(input("Enter the number corresponding to the wordlist .txt file: ").strip()) - 1
        if 0 <= wordlist_index < len(txt_files_in_folder):
            wordlist_file = txt_files_in_folder[wordlist_index]

            found_subdomains = brute_force_subdomains(target_domain, wordlist_file)

            print("\nBrute-force results:")
            for subdomain, info in found_subdomains.items():
                print(f"Subdomain found: {subdomain} (Time: {info['elapsed_time']:.4f} seconds)")

                if info['ip_addresses']:
                    print(f"  IPs: {', '.join(info['ip_addresses'])}")

            report_choice = input("\nDo you want to generate a report? (Y/N): ").strip().lower()

            if report_choice == 'y':
                generate_report(results, found_subdomains)
            else:
                print("Report not generated.")
        else:
            print("Invalid index.")
    else:
        print("Subdomain brute-force skipped.")
