import os

# Enable ANSI escape sequences on Windows
os.system('')

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def main():
    print(f"{Colors.CYAN}{Colors.BOLD}Hello Ninja!{Colors.RESET}")
    print(f"{Colors.BLUE}Welcome to the voting dojo{Colors.RESET}")
    print(f"{Colors.MAGENTA}-------------------------------------------------------------------------{Colors.RESET}")
    
    try:
        name = input(f"{Colors.YELLOW}Please enter your name: {Colors.RESET}")
        age_input = input(f"{Colors.YELLOW}Enter your age: {Colors.RESET}")
        age = int(age_input)
        
        print(f"{Colors.MAGENTA}-------------------------------------------------------------------------{Colors.RESET}")
        
        if age >= 18:
            print(f"{Colors.GREEN}{Colors.BOLD}Awesome {name}! You are {age} years old and eligible to vote in the dojo! 🗳️{Colors.RESET}")
        else:
            years_left = 18 - age
            print(f"{Colors.RED}Sorry {name}, you are only {age}. You need to wait {years_left} more year(s) to vote. 🥋{Colors.RESET}")
            
    except ValueError:
        print(f"{Colors.RED}{Colors.BOLD}Error: Please enter a valid number for your age!{Colors.RESET}")

if __name__ == "__main__":
    main()