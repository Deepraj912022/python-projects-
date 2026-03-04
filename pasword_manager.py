from cryptography.fernet import Fernet
import base64
import hashlib

def load_key():
    with open("key.key", "rb") as file:
        return file.read()

master_pwd = input("What is the master password: ")

# Derive a valid Fernet key
key = load_key()
derived_key = base64.urlsafe_b64encode(
    hashlib.sha256(key + master_pwd.encode()).digest()
)

fer = Fernet(derived_key)

def view():
    try:
        with open("passwords.txt", "r") as f:
            for line in f.readlines():
                data = line.rstrip()
                user, passw = data.split("|")
                print("User:", user, "| Password:", fer.decrypt(passw.encode()).decode())
    except FileNotFoundError:
        print("No passwords saved yet.")

def add():
    name = input("Account Name: ")
    pwd = input("Password: ")

    with open("passwords.txt", "a") as f :
        f.write(name + "|" + str(fer.encrypt(pwd.encode()).decode()) + "\n")

while True:
    mode = input(
        "Would you like to add a new password or view existing ones (add/view)? Press Q to quit: "
    ).lower()

    if mode == "q":
        break
    elif mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")