from .console_view import display
import os
import subprocess

def clear_screen():
    if os.name == 'posix':
        subprocess.run('clear')
    else:
        subprocess.run('cls')

def main():
    clear_screen()
    display(os.name)

if __name__ == "__main__":
    main()