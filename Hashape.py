import hashlib
import itertools
import string
import threading

#algorithm
def hash_string(text, algorithm):
    if algorithm == "md5":
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(text.encode()).hexdigest()
    else:
        raise ValueError("Unsupported hash algorithm")

#brute_force    
def brute_force(hash_to_crack, algorithm, charset, max_length):
    for length in range(1, max_length + 1):
        for attempt in itertools.product(charset, repeat=length):
            attempt = "".join(attempt)
            hashed_attempt = hash_string(attempt, algorithm)
            if hashed_attempt == hash_to_crack:
                print(f"[+] Cracked! The password is : {attempt}")
                return True
    print("[-] Brute-Force failed.")
    return False

#Dictionary_attack
def dictionary_attack(hash_to_crack, algorithm, wordlist_file):
    try:
        with open(wordlist_file, "r") as file:
            for word in file:
                word = word.strip()
                hashed_word == hash_string(word, algorithm)
                if hashed_word == hash_to_crack:
                    print(f"[+] Cracked! The password is: {word}")
                    return True
        print("[-] Dictionary attack Failed")
    except FileNotFoundError:
        print("[-] Error: Wordlist not found!")
    return False

#Multi-Threadung
def threaded_brute_force(hash_to_crack, algorithm, charset, max_length, num_threads):
    def worker(threat_id):
        print(f"[Thread {threat_id}] Starting Brute-Force...")
        brute_force(hash_to_crack,algorithm,charset,max_length)

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(1,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

#What the hash?
def identify_hash(hash_value):
    hash_length = len(hash_value)

    if hash_length == 32:
        return "MD5 (32 characters)"
    elif hash_length == 40:
        return "SHA-1 (40 characters)"
    elif hash_length == 64:
        return "SHA-265 (64 characters)"
    elif hash_length == 128:
        return "SHA-512 (128 characters)"
    else:
        return "Unkown hash type (length doesnt match common hashes)"

#Banner
def show_banner():
    print(r"""
    _    _           _   _               
   | |  | |         | | | |            
   | |__| | __ _ ___| |_| |   __ _ _ __ ___ 
   |  __  |/ _` / __| __| |  / _` | '__/ _ \
   | |  | | (_| \__ \ | | | | (_| | | |  __/
   |_|  |_|\__,_|___/_| |_|  \__,_|_|  \___|
   
                Created by Hanselaffe
    """)

#Show main menu
def show_menu():
    print("======================================")
    print("        HashApe - Hash Cracking Tool")
    print("        Developed by: Hanselaffe")
    print("======================================")
    print("1. Brute Force Attack")
    print("2. Dictionary Attack")
    print("3. Identify Hash Type")
    print("4. Exit")
    print("======================================")

#interactive menu
def main():
    show_banner()
    
    while True:
        show_menu()
        choice = input("Select an option (1/2/3/4): ")
        
        if choice == "1":
            print("\n[*] Brute Force Attack Selected")
            hash_input = input("Enter the hash to crack: ")
            algorithm = input("Enter the hash algorithm (md5/sha256): ").lower()
            charset = string.ascii_lowercase + string.digits  # Definiert den Zeichensatz (kleine Buchstaben + Ziffern)
            max_length = int(input("Enter the maximum password length: "))
            num_threads = int(input("Enter number of threads: "))
            print("[*] Starting Brute-Force Attack...")
            threaded_brute_force(hash_input, algorithm, charset, max_length, num_threads)
        
        elif choice == "2":
            print("\n[*] Dictionary Attack Selected")
            hash_input = input("Enter the hash to crack: ")
            algorithm = input("Enter the hash algorithm (md5/sha256): ").lower()
            wordlist = input("Enter path to wordlist file: ")
            print("[*] Starting Dictionary Attack...")
            dictionary_attack(hash_input, algorithm, wordlist)

        elif choice == "3":
            print("\n[*] Hash Type Identification Selected")
            hash_input = input("Enter the hash to identify: ")
            identified = identify_hash(hash_input)
            print(f"[+] Identified Hash: {identified}")

        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid option. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
