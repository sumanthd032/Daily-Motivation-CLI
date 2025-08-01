# Termi-Vate motivational CLI

![Termi-Vate](https://i.imgur.com/IF42R2y.png)

A fun and powerful command-line utility that delivers a dose of inspiration directly to your terminal. Each time you run the app, it displays a random motivational quote from a customizable list, complete with the current date, time, and a fun emoji.

This tool is packed with features, allowing you to **add** your own favorite quotes, **list** all available quotes, **search** for specific keywords, and even display the **local weather**.

---
## Features
* **Daily Quote**: Get a random motivational quote.
* **Quote of the Day**: Use the `--qotd` flag to see the same quote for the entire day.
* **Weather Display**: Add the `--weather` flag to see your local weather.
* **Quote Management**:
    * `--add 'Your quote'`: Add a new quote to your list.
    * `--list`: View all your saved quotes.
    * `--search 'keyword'`: Find quotes containing a specific keyword.
* **History**:
    * `--history`: View the last 10 quotes that were displayed.
* **Customization**:
    * `--color <COLOR>`: Change the display color (e.g., `red`, `green`, `blue`).
    * `--font <FONT>`: Change the title font style (e.g., `standard`, `slant`, `smslant`, `rectangles`).
* **Shareable Output**:
    * `--share`: Get a clean, text-only version of a random quote to easily copy and paste.

---
## Installation
1.  **Prerequisites**: Make sure you have Python 3.x installed on your system.
2.  **Clone the repository (or save the files)**:
    Save `main.py` and `quotes.txt` in the same directory.
3.  **Install dependencies**:
    Navigate to the project directory in your terminal and run:
    ```bash
    pip install -r requirements.txt
    ```
---
## Usage
Here are some examples of how to use Termi-Vate:

| Command | Description |
| :--- | :--- |
| `python main.py` | Display a random motivational quote. |
| `python main.py --qotd` | Show the quote of the day. |
| `python main.py --weather` | Display a quote with the local weather. |
| `python main.py --add "New quote"` | Add a new quote to your collection. |
| `python main.py --list` | List all available quotes. |
| `python main.py --search "time"`| Search for quotes containing the word "time". |
| `python main.py --history` | View your quote history. |
| `python main.py --color blue` | Change the display color to blue. |
| `python main.py --share` | Get a clean quote for sharing. |
