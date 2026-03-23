import asyncio
import aiohttp
from rich import print

from Validation.Url_Validation import url_validation
from Validation.Wordlist_Validation import wordlist_validation

LFI_SIGNATURES = [
    "root:x:",
    "daemon:x:",
    "[boot loader]",
    "[fonts]",
]


def is_lfi_success(text: str) -> bool:
    return any(signature in text for signature in LFI_SIGNATURES)


def lfi_scanner(url, wordlist, threads, timeout):
    url = url_validation(url)
    wordlist = wordlist_validation(wordlist)

    print(f"[bold red]Url:[bold yellow] {url}")
    print(f"[bold red]Wordlist:[bold yellow] {wordlist}")
    print(f"[bold red]Threads:[bold yellow] {threads}")
    print(f"[bold red]Timeout:[bold yellow] {timeout}")
    print(f"\n[bold yellow]Performing LFI Scan ... [/bold yellow]\n")

    try:
        asyncio.run(lfi_async_scanner(url, wordlist, threads, timeout))
    except KeyboardInterrupt:
        print("[bold red][!] Scan interrupted by user (CTRL+C)[/bold red]")


async def worker(queue, session, base_url, stop_event):
    while not stop_event.is_set():
        try:
            payload = queue.get_nowait()
        except asyncio.QueueEmpty:
            return

        try:
            full_url = base_url + payload
            async with session.get(full_url) as response:
                text = await response.text(errors="ignore")

                if is_lfi_success(text):
                    if not stop_event.is_set():
                        stop_event.set()
                        print(f"[bold green][+] LFI detected with payload: [bold yellow]{payload}")
                    return

        except asyncio.CancelledError:
            raise
        except Exception:
            pass
        finally:
            queue.task_done()


async def lfi_async_scanner(base_url, wordlist, threads, timeout):
    queue = asyncio.Queue()
    stop_event = asyncio.Event()

    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            payload = line.strip()
            if payload:
                queue.put_nowait(payload)

    connector = aiohttp.TCPConnector(limit=threads)
    timeout_cfg = aiohttp.ClientTimeout(total=timeout)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout_cfg) as session:
        tasks = [
            asyncio.create_task(worker(queue, session, base_url, stop_event))
            for _ in range(threads)
        ]

        try:
            await asyncio.gather(*tasks)
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

    if not stop_event.is_set():
        print(f"\n[bold red][-] LFI not detected[/bold red]\n")