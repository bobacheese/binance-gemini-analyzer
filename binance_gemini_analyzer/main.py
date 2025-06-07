import asyncio
import signal
import time
from blessed import Terminal
from pyfiglet import Figlet
from binance_data import get_binance_data
from indicators import calculate_indicators
from gemini_analyzer import analyze_with_gemini
from trading_signals import signal_engine
from config import GEMINI_API_KEY
import pandas as pd

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

def create_advanced_table(data, trading_rec):
    """Membuat tabel informasi trading yang komprehensif"""
    table = "🎯 TRADING DASHBOARD ADVANCED\n"
    table += "=" * 60 + "\n"

    # Price Info
    table += f"💰 HARGA: ${data.get('close', 0):.6f}\n"
    table += f"📊 VOLUME: {data.get('volume', 0):,.0f}\n"
    table += "-" * 60 + "\n"

    # Trading Signals
    table += "🚀 SINYAL TRADING:\n"
    table += f"   Action: {trading_rec.get('action', 'N/A')} ({trading_rec.get('confidence', 0):.1f}%)\n"
    table += f"   Entry: ${trading_rec.get('entry_price', 0):.6f}\n"
    table += f"   Stop Loss: ${trading_rec.get('stop_loss', 0):.6f}\n"
    table += f"   Take Profit 1: ${trading_rec.get('take_profit_1', 0):.6f}\n"
    table += f"   Take Profit 2: ${trading_rec.get('take_profit_2', 0):.6f}\n"
    table += f"   Risk/Reward: {trading_rec.get('risk_reward_ratio', 0):.2f}\n"
    table += "-" * 60 + "\n"

    # Technical Indicators
    table += "📈 INDIKATOR TEKNIKAL:\n"
    table += f"   RSI: {data.get('RSI', 0):.2f}\n"
    table += f"   MACD: {data.get('MACD', 0):.6f}\n"
    table += f"   Signal Score: {data.get('Signal_Score', 0)}\n"
    table += f"   ADX: {data.get('ADX', 0):.2f}\n"
    table += f"   Williams %R: {data.get('Williams_R', 0):.2f}\n"
    table += "-" * 60 + "\n"

    # Risk Metrics
    table += "⚠️ RISK METRICS:\n"
    table += f"   Volatility: {trading_rec.get('volatility', 0):.2f}%\n"
    table += f"   ATR%: {trading_rec.get('atr_percent', 0):.2f}%\n"
    table += f"   Support: ${trading_rec.get('support', 0):.6f}\n"
    table += f"   Resistance: ${trading_rec.get('resistance', 0):.6f}\n"
    table += "-" * 60 + "\n"

    # ML Analysis
    table += "🤖 MACHINE LEARNING:\n"
    table += f"   ML Signal: {trading_rec.get('ml_signal', 0)}\n"
    table += f"   ML Confidence: {trading_rec.get('ml_confidence', 0):.1f}%\n"
    table += f"   Trend Strength: {trading_rec.get('trend_strength', 0):.4f}\n"

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
        
        progress_window = term.green + "🔄 Menghitung indikator advanced..." + term.normal
        display_windows(header, input_window, progress_window, result_window, indicator_window)
        data_with_indicators = calculate_indicators(klines, timeframe)

        progress_window = term.yellow + "🤖 Menganalisis dengan ML & AI..." + term.normal
        display_windows(header, input_window, progress_window, result_window, indicator_window)

        # Generate trading recommendation
        df = pd.DataFrame(data_with_indicators)
        trading_recommendation = signal_engine.generate_trading_recommendation(df, symbol, timeframe)

        progress_window = term.magenta + "🚀 Mengirim ke Gemini untuk analisis final..." + term.normal
        display_windows(header, input_window, progress_window, result_window, indicator_window)
        analysis = await analyze_with_gemini(data_with_indicators, GEMINI_API_KEY, symbol, timeframe)

        result_window = term.bold_white + "🎯 HASIL ANALISIS AI:\n" + term.normal + analysis

        last_data = data_with_indicators[-1]
        indicator_window = term.cyan + create_advanced_table(last_data, trading_recommendation) + term.normal
        
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
