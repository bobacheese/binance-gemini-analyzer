import aiohttp
import asyncio
from rich.console import Console

console = Console()
BASE_URL = "https://api.binance.com/api/v3/klines"

async def get_binance_data(symbol, interval, limit=1000):
    async with aiohttp.ClientSession() as session:
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        
        console.log(f"[bold blue]Requesting data from Binance:[/bold blue] {BASE_URL}")
        console.log(f"[blue]Params:[/blue] {params}")
        
        async with session.get(BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                console.log(f"[green]Successfully fetched {len(data)} candles[/green]")
                return data
            else:
                console.log(f"[bold red]Error: {response.status}[/bold red]")
                console.log(f"[red]Response: {await response.text()}[/red]")
                return None
