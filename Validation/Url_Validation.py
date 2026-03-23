from urllib.parse import urlparse
import sys
from rich import print

def url_validation(url):

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):raise ValueError("[bold red] Invalid URL scheme.[/bold red] \n""Use http:// or https://")
        if not parsed.netloc:raise ValueError("[bold red] Invalid URL format.\n[/bold red] ""Example: http://victim.com/index.php?page=")
        if not parsed.query or "=" not in parsed.query:raise ValueError("[bold red] Missing parameter.[/bold red] \n""Example: http://victim.com/index.php?page=")

        param_name = parsed.query.split("=", 1)[0]

        if not param_name:raise ValueError("[bold red] Parameter name is missing.[/bold red] \n""Example: http://victim.com/index.php?page=")
        if not url.endswith("="):raise ValueError("[bold red] URL must end with '=' for payload injection.[/bold red] \n""Example: http://victim.com/index.php?page=")

        return url

    except ValueError as e:
        print(f"ValueError: [bold red] {e} [/bold red]")
        sys.exit(1)
