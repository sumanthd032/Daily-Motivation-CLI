
import random
import datetime
import argparse
import sys
import requests
import os
import json

try:
    import pyfiglet
except ImportError:
    pyfiglet = None

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class DummyStyle:
        def __getattr__(self, name):
            return ""
    Fore = DummyStyle()
    Style = DummyStyle()


QUOTES_FILE = "quotes.txt"
HISTORY_FILE = ".quote_history.json"
QOTD_FILE = ".qotd.json"
EMOJIS = ["🚀", "✨", "🎉", "💪", "🔥", "🌟", "💡", "💯", "✅", "🎯"]
LOCATION = "Udupi,Karnataka,India"
AVAILABLE_COLORS = {
    'black': Fore.BLACK, 'red': Fore.RED, 'green': Fore.GREEN,
    'yellow': Fore.YELLOW, 'blue': Fore.BLUE, 'magenta': Fore.MAGENTA,
    'cyan': Fore.CYAN, 'white': Fore.WHITE,
}



def manage_quotes(args):
    """Handles all quote management actions."""
    quotes = get_quotes_from_file()

    if args.add:
        add_quote(args.add)
    elif args.list:
        list_quotes(quotes)
    elif args.search:
        search_quotes(quotes, args.search)
    elif args.history:
        show_history()
    elif args.share:
        share_quote(quotes)

def get_quotes_from_file():
    """Reads all quotes from the quotes file."""
    if not os.path.exists(QUOTES_FILE):
        print(f"{Fore.RED}Error: The file '{QUOTES_FILE}' was not found.")
        sys.exit(1)
    with open(QUOTES_FILE, 'r') as file:
        return [line.strip() for line in file if line.strip()]

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
        response = requests.get(f'https://wttr.in/{LOCATION}?format=3')
        return response.text.strip() if response.status_code == 200 else "Weather data unavailable."
    except requests.RequestException:
        return "Could not connect to weather service."

def log_quote_history(quote):
    """Logs the displayed quote to a history file."""
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    history.insert(0, {'quote': quote, 'timestamp': datetime.datetime.now().isoformat()})
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history[:10], f, indent=2) 

def show_history():
    """Displays the last 10 quotes from history."""
    print(f"{Style.BRIGHT}{Fore.YELLOW}--- Quote History ---")
    if not os.path.exists(HISTORY_FILE):
        print(f"{Fore.CYAN}No history found.")
        return
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)
    for item in history:
        ts = datetime.datetime.fromisoformat(item['timestamp']).strftime('%Y-%m-%d %H:%M')
        print(f"{Fore.CYAN}[{ts}] {item['quote']}")

def get_qotd(quotes):
    """Gets the quote of the day, generating a new one if the day has changed."""
    today = datetime.date.today().isoformat()
    qotd_data = {}
    if os.path.exists(QOTD_FILE):
        with open(QOTD_FILE, 'r') as f:
            qotd_data = json.load(f)

    if qotd_data.get('date') == today:
        return qotd_data['quote']

    new_quote = random.choice(quotes)
    with open(QOTD_FILE, 'w') as f:
        json.dump({'date': today, 'quote': new_quote}, f)
    return new_quote

def share_quote(quotes):
    """Prints a clean version of a random quote for easy sharing."""
    print(random.choice(quotes))

def display_motivation(args):
    """Generates and displays the main motivational message."""
    quotes = get_quotes_from_file()
    if not quotes:
        print(f"{Fore.RED}No quotes found in {QUOTES_FILE}. Add some with --add.")
        return

    quote = get_qotd(quotes) if args.qotd else random.choice(quotes)
    log_quote_history(quote)

    random_emoji = random.choice(EMOJIS)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = AVAILABLE_COLORS.get(args.color.lower(), Fore.MAGENTA) if args.color else Fore.MAGENTA

    print(f"{Style.BRIGHT}{color}" + "+" + "-" * 60 + "+")

    if pyfiglet:
        font = args.font if args.font else 'slant'
        try:
            ascii_title = pyfiglet.figlet_format("Termi-Vate", font=font)
            print(f"{Fore.GREEN}{ascii_title.strip()}")
        except pyfiglet.FontNotFound:
            print(f"{Fore.RED}Font '{font}' not found. Using default.")
            ascii_title = pyfiglet.figlet_format("Termi-Vate", font='slant')
            print(f"{Fore.GREEN}{ascii_title.strip()}")
    else:
        print(f"{Fore.GREEN}{'Termi-Vate'.center(60)}")

    print(f"{Style.BRIGHT}{color}" + "-" * 62)
    print(f"  {Fore.CYAN}{quote.center(58)}  ")
    print(f"{Style.BRIGHT}{color}" + "+" + "-" * 60 + "+")

    info_line = f" {current_time.ljust(30)} {random_emoji.rjust(27)} "
    print(f"|{Fore.YELLOW}{info_line}|")

    if args.weather:
        weather = get_weather()
        weather_line = f" {weather.ljust(58)} "
        print(f"|{Fore.BLUE}{weather_line}|")

    print(f"{Style.BRIGHT}{color}" + "+" + "-" * 60 + "+")

# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Termi-Vate: A command-line tool for a dose of daily motivation.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # Group for display actions
    display_group = parser.add_argument_group('Display Options')
    display_group.add_argument('--weather', action='store_true', help="Display current weather information.")
    display_group.add_argument('--qotd', action='store_true', help="Show the quote of the day.")
    display_group.add_argument('--color', type=str, help=f"Change display color. Available: {', '.join(AVAILABLE_COLORS.keys())}")
    display_group.add_argument('--font', type=str, help="Change title font (e.g., standard, slant, smslant).")

    # Group for quote management
    mgmt_group = parser.add_argument_group('Quote Management')
    mgmt_group.add_argument('--add', type=str, help="Add a new quote to the list.")
    mgmt_group.add_argument('--list', action='store_true', help="List all available quotes.")
    mgmt_group.add_argument('--search', type=str, help="Search for quotes containing a keyword.")
    mgmt_group.add_argument('--history', action='store_true', help="Show the last 10 quotes.")
    mgmt_group.add_argument('--share', action='store_true', help="Get a clean quote for sharing.")


    args = parser.parse_args()

    if any([args.add, args.list, args.search, args.history, args.share]):
        manage_quotes(args)
    else:
        display_motivation(args)
