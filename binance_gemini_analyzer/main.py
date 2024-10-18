import asyncio
import signal
import time
from blessed import Terminal
from pyfiglet import Figlet
from binance_data import get_binance_data
from indicators import calculate_indicators
from gemini_analyzer import analyze_with_gemini
from config import GEMINI_API_KEY

term = Terminal()

def handle_sigint(signum, frame):
    print(term.clear)
    print(term.bold_red + "\nProgram dihentikan oleh user!" + term.normal)
    exit(0)

signal.signal(signal.SIGINT, handle_sigint)

def create_header():
    f = Figlet(font='slant')
    header_text = f.renderText("Binance Gemini Analyzer")
    subheader = "dibuat oleh bobacheese"
    
    return (term.bold_magenta + header_text + term.normal +
            term.move_x(term.width // 2 - len(subheader) // 2) +
            term.cyan + subheader + term.normal)

def create_table(data):
    table = "Ringkasan Indikator Terakhir:\n"
    table += "-" * 40 + "\n"
    table += f"{'Indikator':<20}{'Nilai':<20}\n"
    table += "-" * 40 + "\n"
    for key, value in data.items():
        if key not in ['timestamp', 'open', 'high', 'low', 'close', 'volume']:
            value_str = f"{value:.4f}" if isinstance(value, float) else str(value)
            table += f"{key:<20}{value_str:<20}\n"
    return table

def display_windows(header, input_window, progress_window, result_window, indicator_window):
    print(term.clear + term.home + header)
    print(term.move_y(term.height // 4) + input_window)
    print(term.move_y(term.height // 2) + progress_window)
    print(term.move_y(term.height // 2 + 5) + result_window)
    print(term.move_y(term.height - 15) + indicator_window)

async def main():
    header = create_header()
    
    while True:
        input_window = ""
        progress_window = ""
        result_window = ""
        indicator_window = ""
        
        display_windows(header, input_window, progress_window, result_window, indicator_window)
        
        symbol = input(term.bold_yellow + "Masukkin pair (contoh: BTCUSDT): " + term.normal).upper()
        timeframe = input(term.bold_yellow + "Pilih timeframe (1m, 5m, 15m, 1h, 4h, 1d): " + term.normal)
        
        input_window = f"Pair: {symbol}\nTimeframe: {timeframe}"
        display_windows(header, input_window, progress_window, result_window, indicator_window)
        
        progress_window = term.cyan + "Ngambil data dari Binance..." + term.normal
        display_windows(header, input_window, progress_window, result_window, indicator_window)
        klines = await get_binance_data(symbol, timeframe)
        
        if not klines:
            progress_window = term.bold_red + "Gagal ngambil data. Coba lagi ya!" + term.normal
            display_windows(header, input_window, progress_window, result_window, indicator_window)
            time.sleep(2)
            continue
        
        progress_window = term.green + "Ngitung indikator..." + term.normal
        display_windows(header, input_window, progress_window, result_window, indicator_window)
        data_with_indicators = calculate_indicators(klines, timeframe)
        
        progress_window = term.magenta + "Ngirim data ke Gemini buat dianalisis..." + term.normal
        display_windows(header, input_window, progress_window, result_window, indicator_window)
        analysis = await analyze_with_gemini(data_with_indicators, GEMINI_API_KEY, symbol, timeframe)
        
        result_window = term.bold_white + "Hasil Analisis Gemini:\n" + term.normal + analysis
        
        last_data = data_with_indicators[-1]
        indicator_window = term.cyan + create_table(last_data) + term.normal
        
        display_windows(header, input_window, progress_window, result_window, indicator_window)
        
        lanjut = input(term.bold_green + "\nMau analisis lagi? (y/n): " + term.normal)
        if lanjut.lower() != 'y':
            break
    
    print(term.clear)
    print(term.bold_cyan + "Makasih udah pake Binance Gemini Analyzer!" + term.normal)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(term.clear)
        print(term.bold_red + "\nProgram dihentikan oleh user. Dadah!" + term.normal)
