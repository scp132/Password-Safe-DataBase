import os
import random
import string
from datetime import datetime

from colorama import init, Fore
from cryptography.fernet import Fernet

init(autoreset=True)

# 📁 Имя файла и ключ шифрования
DATABASE_FILE = "P.S.B.txt"
KEY_FILE = "key.key"


# ====== Шифрование ======

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key


FERNET = Fernet(load_key())


def encrypt(data: str) -> bytes:
    return FERNET.encrypt(data.encode())


def decrypt(data: bytes) -> str:
    return FERNET.decrypt(data).decode()


# ====== UI ======

def show_ascii():
    ascii_art = f"""
{Fore.BLUE}
oooooooooo        oooooooo8       oooooooooo 
 888    888      888               888    888
 888oooo88        888oooooo        888oooo88 
 888                     888       888    888
o888o            o88oooo888       o888ooo888 
"""
    print(ascii_art)


def show_menu():
    print(f"{Fore.GREEN}1. Generate Password")
    print(f"{Fore.GREEN}2. Search Password")
    print(f"{Fore.GREEN}3. Change Password/Login")
    print(f"{Fore.GREEN}4. Credits")
    print(f"{Fore.GREEN}5. Exit")
    print(f"{Fore.GREEN}6. View All Passwords\n")


# ====== Core Logic ======

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


def add_password():
    password = generate_password()
    print(f"\nGenerated Password: {Fore.YELLOW}{password}")

    login = input("Enter Login/User: ")
    site = input("Enter Site URL: ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"{password} | {login} | {site} | {date}\n"

    encrypted_line = encrypt(line)
    with open(DATABASE_FILE, "ab") as f:
        f.write(encrypted_line + b'\n')

    print(f"{Fore.GREEN}Password saved to encrypted database.\n")


def read_all():
    if not os.path.exists(DATABASE_FILE):
        return []
    with open(DATABASE_FILE, "rb") as f:
        lines = f.readlines()
    decrypted = []
    for line in lines:
        line = line.strip()
        if line:
            try:
                decrypted.append(decrypt(line))
            except:
                print(f"{Fore.RED}Warning: corrupted line skipped.")
    return decrypted


def search_password():
    url = input("Enter Site URL to search: ")
    found = []
    records = read_all()
    for line in records:
        if url in line:
            parts = line.strip().split("|")
            if len(parts) == 4:
                found.append(f"{parts[0].strip()} | {parts[1].strip()} | {parts[3].strip()}")
    if found:
        print("\nResults:")
        for item in found:
            print(item)
    else:
        print(f"{Fore.RED}No records found for {url}.\n")


def change_entry():
    print(f"\n{Fore.GREEN}1. Change Login/User")
    print(f"{Fore.GREEN}2. Change Password")
    option = input("Choose option: ")

    url = input("Enter Site URL: ")
    records = read_all()

    entries = []
    for idx, line in enumerate(records):
        if url in line:
            parts = line.strip().split("|")
            if len(parts) == 4:
                entries.append((idx, parts))

    if not entries:
        print(f"{Fore.RED}No entries found for {url}.\n")
        return

    print("\nFound Entries:")
    for i, (idx, parts) in enumerate(entries):
        print(f"{i + 1}. {parts[1].strip()} | {parts[0].strip()} | {parts[3].strip()}")

    choice = int(input("Choose number to edit: ")) - 1

    idx_to_edit, parts = entries[choice]
    new_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if option == "1":
        new_login = input("Enter New Login/User: ")
        parts[1] = f" {new_login} "
    elif option == "2":
        new_password = generate_password()
        print(f"New Generated Password: {Fore.YELLOW}{new_password}")
        parts[0] = f"{new_password} "
    else:
        print(f"{Fore.RED}Invalid option.\n")
        return

    parts[3] = f" {new_date}"
    new_line = "|".join(parts) + "\n"
    records[idx_to_edit] = new_line

    with open(DATABASE_FILE, "wb") as f:
        for record in records:
            encrypted_line = encrypt(record)
            f.write(encrypted_line + b'\n')

    print(f"{Fore.GREEN}Entry updated successfully!\n")


def view_all_passwords():
    records = read_all()
    if not records:
        print(f"{Fore.RED}Database is empty or corrupted.\n")
        return
    print("\nAll Passwords:")
    for record in records:
        parts = record.strip().split("|")
        if len(parts) == 4:
            # PASSWORD | LOGIN | URL | DATE => rearrange to URL | LOGIN | PASSWORD | DATE
            print(f"{parts[2].strip()} | {parts[1].strip()} | {parts[0].strip()} | {parts[3].strip()}")
    print()


def show_credits():
    credits_ascii = f"""
{Fore.BLUE}
     o             oooooooo8      ooooo            oooo   oooo
    888          o888     88       888              888  o88  
   8  88         888               888              888888    
  8oooo88        888o     oo       888      o       888  88o  
o88o  o888o       888oooo88       o888ooooo88      o888o o888o
 CREATED BY ACLK COMPANY
"""
    print(credits_ascii)


def main():
    while True:
        show_ascii()
        show_menu()
        choice = input("Choose option: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            search_password()
        elif choice == "3":
            change_entry()
        elif choice == "4":
            show_credits()
        elif choice == "5":
            print(f"{Fore.GREEN}Goodbye!")
            break
        elif choice == "6":
            view_all_passwords()
        else:
            print(f"{Fore.RED}Invalid option, try again.\n")


if __name__ == "__main__":
    main()
