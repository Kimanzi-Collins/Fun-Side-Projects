import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.align import Align
from rich.text import Text

console = Console()

# Curated DC Universe Database
dc_database = [
    # Cartoons
    {"title": "Batman: The Animated Series", "type": "Cartoon", "year": "1992", "imdb": "9.0", "cover": "🦇 🌃 🃏", "color": "yellow"},
    {"title": "Justice League Unlimited", "type": "Cartoon", "year": "2004", "imdb": "8.7", "cover": "🌎 🦸‍♂️ ⚡", "color": "blue"},
    {"title": "Young Justice", "type": "Cartoon", "year": "2010", "imdb": "8.6", "cover": "👦 🦸‍♀️ 🏹", "color": "green"},
    {"title": "Teen Titans", "type": "Cartoon", "year": "2003", "imdb": "7.9", "cover": "👽 🤖 🐦", "color": "magenta"},
    
    # Series
    {"title": "Peacemaker", "type": "Series", "year": "2022", "imdb": "8.3", "cover": "🕊️ 🔫 🦅", "color": "red"},
    {"title": "Doom Patrol", "type": "Series", "year": "2019", "imdb": "7.8", "cover": "🧠 🤖 🩹", "color": "cyan"},
    {"title": "The Flash", "type": "Series", "year": "2014", "imdb": "7.5", "cover": "⚡ 🏃‍♂️ ⏱️", "color": "red"},
    {"title": "Arrow", "type": "Series", "year": "2012", "imdb": "7.5", "cover": "🏹 🟢 🎯", "color": "green"},
    
    # Movies
    {"title": "The Dark Knight", "type": "Movie", "year": "2008", "imdb": "9.0", "cover": "🦇 🤡 🪙", "color": "bright_black"},
    {"title": "The Batman", "type": "Movie", "year": "2022", "imdb": "7.8", "cover": "🦇 ❓ 🌧️", "color": "red"},
    {"title": "Wonder Woman", "type": "Movie", "year": "2017", "imdb": "7.4", "cover": "🛡️ ⚔️ 🌟", "color": "gold1"},
    {"title": "Superman", "type": "Movie", "year": "1978", "imdb": "7.3", "cover": "🦸‍♂️ 👓 ☄️", "color": "blue"},
]

def boot_sequence():
    """Simulates a dramatic booting sequence for the terminal interface."""
    console.clear()
    
    welcome_text = Text("\nINITIALIZING WAYNE ENTERPRISES SATELLITE UPLINK...\n", style="bold green")
    console.print(welcome_text, justify="center")
    time.sleep(1)

    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="blue", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=True
    ) as progress:
        task1 = progress.add_task("[red]Decrypting ARGUS files...", total=100)
        task2 = progress.add_task("[blue]Connecting to the Watchtower...", total=100)
        task3 = progress.add_task("[yellow]Loading Batcomputer Archives...", total=100)

        while not progress.finished:
            progress.update(task1, advance=2)
            progress.update(task2, advance=1.5)
            progress.update(task3, advance=3)
            time.sleep(0.05)

def display_interface():
    """Builds and displays the main DC UI."""
    console.clear()
    
    # Header
    header = Panel(
        Align.center("[bold bright_white]DC UNIVERSE TERMINAL[/bold bright_white]\n[blue]Watchtower Access Granted[/blue] | [red]Clearance Level: Omega[/red]"),
        border_style="bold blue",
        padding=(1, 2)
    )
    console.print(header)
    console.print("\n")

    # Main Data Table
    table = Table(show_header=True, header_style="bold gold1", border_style="bright_black", expand=True)
    
    table.add_column("Cover Art", justify="center", width=12)
    table.add_column("Title", style="bold white", width=30)
    table.add_column("Format", justify="center", width=10)
    table.add_column("Year", justify="center", style="dim", width=6)
    table.add_column("IMDb", justify="center", width=8)

    # Sort database by IMDb rating (highest first)
    sorted_db = sorted(dc_database, key=lambda x: float(x["imdb"]), reverse=True)

    for item in sorted_db:
        # Format the IMDb rating to have a star
        imdb_formatted = f"[bold yellow]⭐ {item['imdb']}[/bold yellow]"
        
        # Color code the format type
        format_style = ""
        if item["type"] == "Movie":
            format_style = "[bold blue]Movie[/]"
        elif item["type"] == "Series":
            format_style = "[bold red]Series[/]"
        elif item["type"] == "Cartoon":
            format_style = "[bold green]Cartoon[/]"

        table.add_row(
            f"[{item['color']}]{item['cover']}[/]",
            item["title"],
            format_style,
            item["year"],
            imdb_formatted
        )

    console.print(table)
    console.print("\n[dim italic]Press Ctrl+C to exit terminal.[/dim italic]")

if __name__ == "__main__":
    try:
        boot_sequence()
        display_interface()
    except KeyboardInterrupt:
        console.print("\n[bold red]Connection terminated by user. Logging out...[/bold red]")