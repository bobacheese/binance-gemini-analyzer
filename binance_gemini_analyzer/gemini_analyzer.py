import aiohttp
import json
from rich.console import Console

console = Console()
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

async def analyze_with_gemini(data, api_key, symbol, timeframe):
    headers = {
        "Content-Type": "application/json"
    }
    
    #prompt
    prompt = f"""
    Analisis data trading berikut untuk {symbol} pada timeframe {timeframe}:

    Data terakhir:
    {json.dumps(data[-1], indent=2)}

    Data sebelumnya:
    {json.dumps(data[-2], indent=2)}

    Berikan analisis mendalam dan rekomendasi trading dengan format berikut:

    1. Analisis Tren Harga:
       - Tren jangka pendek:
       - Tren jangka menengah:
       - Support dan resistance terdekat:

    2. Analisis Indikator Teknikal:
       - MACD:
       - RSI:
       - Bollinger Bands:
       - Stochastic Oscillator:
       - Moving Averages:

    3. Rekomendasi Trading:
       - Posisi: [Beli/Jual/Hold]
       - Entry Price:
       - Take Profit 1:
       - Take Profit 2:
       - Stop Loss:
       - Risk/Reward Ratio:

    4. Tingkat Keyakinan Analisis: [dari 0 sampai 100%]

    5. Alasan Rekomendasi:
       [Jelaskan alasan di balik rekomendasi trading]

    6. Faktor Penting Lainnya:
       - Volatilitas:
       - Volume:
       - Sentimen Pasar:

    7. Manajemen Risiko:
       [Berikan saran manajemen risiko]

    8. Timeframe yang Disarankan:
       [Berikan saran timeframe terbaik untuk trade ini]

    Berikan analisis yang objektif dan informatif berdasarkan data yang tersedia.
    """
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    url = f"{GEMINI_API_URL}?key={api_key}"
    
    console.log(f"[bold blue]Ngirim request ke Gemini API:[/bold blue] {GEMINI_API_URL}")
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                result = await response.json()
                console.log("[green]Berhasil dapet analisis dari Gemini[/green]")
                analysis_text = result['candidates'][0]['content']['parts'][0]['text']
                return analysis_text
            else:
                error_msg = f"Error: {response.status} - {await response.text()}"
                console.log(f"[bold red]{error_msg}[/bold red]")
                return error_msg
