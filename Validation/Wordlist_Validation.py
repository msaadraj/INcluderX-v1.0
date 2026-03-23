import os
import sys
from rich import print

def wordlist_validation(wordlist):
    try:
        if not wordlist:
            default_path = os.path.join("Wordlists", "LFI.txt")
            if not os.path.isfile(default_path):
                raise ValueError("[bold red] Default wordlist not found.[/bold red] \n""Expected: Wordlist/RFI.txt")
            return default_path
        if not os.path.isfile(wordlist):raise ValueError(f"Wordlist not found: [bold red]{wordlist}[/bold red]")

        return wordlist

    except ValueError as e:
        print(f"ValueError: [bold red] {e}[/bold red]")
        sys.exit(1)
