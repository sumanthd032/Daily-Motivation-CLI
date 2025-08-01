# main.py
import random
import datetime
import argparse
import sys
import requests

# Attempt to import optional styling libraries
try:
    import pyfiglet
except ImportError:
    pyfiglet = None

try:
    from colorama import Fore, Style, init
    init(autoreset=True) # Initialize colorama
except ImportError:
    # Create dummy Fore and Style classes if colorama is not installed
    class DummyStyle:
        def __getattr__(self, name):
            return ""
    Fore = DummyStyle()
    Style = DummyStyle()


# --- Configuration ---
QUOTES_FILE = "quotes.txt"
EMOJIS = ["🚀", "✨", "🎉", "💪", "🔥", "🌟", "💡", "💯", "✅", "🎯"]
LOCATION = "Udupi,Karnataka,India"

# --- Core Functions ---

def manage_quotes(args):
    """Handles adding, listing, and searching quotes."""
    quotes = get_quotes_from_file()

    if args.add:
        add_quote(args.add)
    elif args.list:
        list_quotes(quotes)
    elif args.search:
        search_quotes(quotes, args.search)

def get_quotes_from_file():
    """Reads all quotes from the quotes file."""
    try:
        with open(QUOTES_FILE, 'r') as file:
            quotes = [line.strip() for line in file if line.strip()]
        return quotes
    except FileNotFoundError:
        print(f"{Fore.RED}Error: The file '{QUOTES_FILE}' was not found.")
        sys.exit(1) # Exit if the core quotes file is missing
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}")
        sys.exit(1)

def add_quote(new_quote):
    """Adds a new quote to the file."""
    with open(QUOTES_FILE, 'a') as file:
        file.write(f"\n{new_quote}")
    print(f"{Fore.GREEN}Success! Your quote has been added.")

def list_quotes(quotes):
    """Displays all available quotes."""
    print(f"{Style.BRIGHT}{Fore.YELLOW}--- All Available Quotes ---")
    if not quotes:
        print(f"{Fore.CYAN}No quotes found.")
        return
    for i, quote in enumerate(quotes, 1):
        print(f"{Fore.CYAN}{i}. {quote}")

def search_quotes(quotes, keyword):
    """Searches for quotes containing a specific keyword."""
    print(f"{Style.BRIGHT}{Fore.YELLOW}--- Quotes matching '{keyword}' ---")
    found_quotes = [q for q in quotes if keyword.lower() in q.lower()]
    if not found_quotes:
        print(f"{Fore.CYAN}No quotes found with that keyword.")
        return
    for i, quote in enumerate(found_quotes, 1):
        print(f"{Fore.CYAN}{i}. {quote}")

def get_weather():
    """Fetches and formats weather for the configured location."""
    try:
        # A free weather API that doesn't require an API key
        response = requests.get(f'https://wttr.in/{LOCATION}?format=3')
        if response.status_code == 200:
            return response.text.strip()
        return "Weather data unavailable."
    except requests.RequestException:
        return "Could not connect to weather service."

def display_motivation(show_weather=False):
    """Generates and displays the main motivational message."""
    quotes = get_quotes_from_file()
    if not quotes:
        random_quote = "No quotes found. Add some using --add 'Your quote'"
    else:
        random_quote = random.choice(quotes)

    random_emoji = random.choice(EMOJIS)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Presentation ---
    print(f"{Style.BRIGHT}{Fore.MAGENTA}" + "+" + "-" * 60 + "+")

    if pyfiglet:
        ascii_title = pyfiglet.figlet_format("MOTIVATE", font="slant")
        print(f"{Fore.GREEN}{ascii_title.strip()}")
    else:
        print(f"{Fore.GREEN}{'MOTIVATE'.center(60)}")

    print(f"{Style.BRIGHT}{Fore.MAGENTA}" + "-" * 62)
    print(f"  {Fore.CYAN}{random_quote.center(58)}  ")
    print(f"{Style.BRIGHT}{Fore.MAGENTA}" + "+" + "-" * 60 + "+")

    info_line = f" {current_time.ljust(30)} {random_emoji.rjust(27)} "
    print(f"|{Fore.YELLOW}{info_line}|")

    if show_weather:
        weather = get_weather()
        weather_line = f" {weather.ljust(58)} "
        print(f"|{Fore.BLUE}{weather_line}|")

    print(f"{Style.BRIGHT}{Fore.MAGENTA}" + "+" + "-" * 60 + "+")


# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A command-line tool for a dose of daily motivation."
    )
    parser.add_argument(
        '--add',
        type=str,
        help="Add a new quote to the list. Usage: --add 'Your new quote'"
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help="List all available quotes."
    )
    parser.add_argument(
        '--search',
        type=str,
        help="Search for quotes containing a keyword."
    )
    parser.add_argument(
        '--weather',
        action='store_true',
        help="Display current weather information."
    )

    args = parser.parse_args()

    # If any command-line argument is used, perform that action.
    # Otherwise, display the default motivation.
    if args.add or args.list or args.search:
        manage_quotes(args)
    else:
        display_motivation(show_weather=args.weather)
