#!/usr/bin/env python3
"""
Test script untuk Binance Gemini Analyzer Advanced
"""
import asyncio
import sys
sys.path.append('.')
from binance_data import get_binance_data
from indicators import calculate_indicators
from trading_signals import signal_engine
import pandas as pd

async def test_analysis():
    print('🚀 Testing Binance Gemini Analyzer Advanced...')
    
    # Test dengan BTCUSDT
    symbol = 'BTCUSDT'
    timeframe = '1h'
    
    print(f'📊 Mengambil data {symbol} timeframe {timeframe}...')
    klines = await get_binance_data(symbol, timeframe, limit=100)
    
    if klines:
        print(f'✅ Berhasil mengambil {len(klines)} data candle')
        
        print('🔄 Menghitung indikator teknikal...')
        data_with_indicators = calculate_indicators(klines, timeframe)
        
        print(f'✅ Berhasil menghitung {len(data_with_indicators)} data dengan indikator')
        
        # Test trading signals
        df = pd.DataFrame(data_with_indicators)
        trading_rec = signal_engine.generate_trading_recommendation(df, symbol, timeframe)
        
        print('\n🎯 HASIL ANALISIS:')
        print(f'Symbol: {trading_rec["symbol"]}')
        print(f'Action: {trading_rec["action"]}')
        print(f'Confidence: {trading_rec["confidence"]}%')
        print(f'Entry Price: ${trading_rec["entry_price"]}')
        print(f'Stop Loss: ${trading_rec["stop_loss"]}')
        print(f'Take Profit 1: ${trading_rec["take_profit_1"]}')
        print(f'Risk/Reward: {trading_rec["risk_reward_ratio"]}')
        print(f'Technical Score: {trading_rec["technical_score"]}')
        print(f'ML Signal: {trading_rec["ml_signal"]}')
        print(f'Volatility: {trading_rec["volatility"]}%')
        
        # Show latest indicators
        latest = data_with_indicators[-1]
        print('\n📈 INDIKATOR TERAKHIR:')
        print(f'RSI: {latest.get("RSI", 0):.2f}')
        print(f'MACD: {latest.get("MACD", 0):.6f}')
        print(f'Signal Score: {latest.get("Signal_Score", 0)}')
        print(f'ADX: {latest.get("ADX", 0):.2f}')
        print(f'Williams %R: {latest.get("Williams_R", 0):.2f}')
        print(f'Recommendation: {latest.get("Recommendation", "N/A")}')
        
        # Test dengan beberapa pair lain
        test_pairs = ['ETHUSDT', 'ADAUSDT', 'SOLUSDT']
        print('\n🔍 Testing dengan pair lain:')
        
        for test_symbol in test_pairs:
            try:
                test_klines = await get_binance_data(test_symbol, '15m', limit=50)
                if test_klines:
                    test_data = calculate_indicators(test_klines, '15m')
                    test_df = pd.DataFrame(test_data)
                    test_rec = signal_engine.generate_trading_recommendation(test_df, test_symbol, '15m')
                    print(f'{test_symbol}: {test_rec["action"]} ({test_rec["confidence"]:.1f}%)')
            except Exception as e:
                print(f'{test_symbol}: Error - {e}')
        
        print('\n✅ Test berhasil! Program siap digunakan.')
    else:
        print('❌ Gagal mengambil data dari Binance')

if __name__ == "__main__":
    asyncio.run(test_analysis())
