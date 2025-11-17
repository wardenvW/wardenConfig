from .console_view import display
from time import sleep
import os
import subprocess

def clear_screen():
    if os.name == 'posix':
        subprocess.run('clear')
    else:
        subprocess.run('cls')

def main():
    os_name = os.name
    clear_screen()
    try:
        while True:
            display(os_name)
            sleep(3)
    except KeyboardInterrupt:
        print("\nleaving wconfig.")

if __name__ == "__main__":
    main()