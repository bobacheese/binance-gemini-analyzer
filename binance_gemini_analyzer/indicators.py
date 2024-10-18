import numpy as np
import pandas as pd
from rich.console import Console

console = Console()

def get_indicator_params(timeframe):
    if timeframe in ['1m', '5m']:
        return {
            'sma_fast': 10, 'sma_slow': 30,
            'ema_fast': 6, 'ema_slow': 13,
            'rsi_period': 7,
            'bb_period': 10, 'bb_std': 2,
            'macd_fast': 6, 'macd_slow': 13, 'macd_signal': 4,
            'stoch_k': 5, 'stoch_d': 3,
            'atr_period': 7
        }
    elif timeframe in ['15m', '30m', '1h']:
        return {
            'sma_fast': 20, 'sma_slow': 50,
            'ema_fast': 12, 'ema_slow': 26,
            'rsi_period': 14,
            'bb_period': 20, 'bb_std': 2,
            'macd_fast': 12, 'macd_slow': 26, 'macd_signal': 9,
            'stoch_k': 14, 'stoch_d': 3,
            'atr_period': 14
        }
    else:  # 4h, 1d
        return {
            'sma_fast': 50, 'sma_slow': 200,
            'ema_fast': 21, 'ema_slow': 55,
            'rsi_period': 21,
            'bb_period': 50, 'bb_std': 2,
            'macd_fast': 21, 'macd_slow': 55, 'macd_signal': 13,
            'stoch_k': 21, 'stoch_d': 7,
            'atr_period': 21
        }

def calculate_indicators(klines, timeframe):
    console.log("[bold green]Mulai ngitung indikator...[/bold green]")
    
    params = get_indicator_params(timeframe)
    
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['volume'] = df['volume'].astype(float)

    console.log("[green]Data dasar udah dikonversi[/green]")

    # SMA
    df[f'SMA_{params["sma_fast"]}'] = df['close'].rolling(window=params['sma_fast']).mean()
    df[f'SMA_{params["sma_slow"]}'] = df['close'].rolling(window=params['sma_slow']).mean()

    # EMA
    df[f'EMA_{params["ema_fast"]}'] = df['close'].ewm(span=params['ema_fast'], adjust=False).mean()
    df[f'EMA_{params["ema_slow"]}'] = df['close'].ewm(span=params['ema_slow'], adjust=False).mean()

    # MACD
    df['MACD'] = df[f'EMA_{params["ema_fast"]}'] - df[f'EMA_{params["ema_slow"]}']
    df['MACD_Signal'] = df['MACD'].ewm(span=params['macd_signal'], adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']

    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=params['rsi_period']).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=params['rsi_period']).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Bollinger Bands
    df['BB_Middle'] = df['close'].rolling(window=params['bb_period']).mean()
    bb_std = df['close'].rolling(window=params['bb_period']).std()
    df['BB_Upper'] = df['BB_Middle'] + (bb_std * params['bb_std'])
    df['BB_Lower'] = df['BB_Middle'] - (bb_std * params['bb_std'])

    # Stochastic Oscillator
    df['Lowest_Low'] = df['low'].rolling(window=params['stoch_k']).min()
    df['Highest_High'] = df['high'].rolling(window=params['stoch_k']).max()
    df['%K'] = (df['close'] - df['Lowest_Low']) / (df['Highest_High'] - df['Lowest_Low']) * 100
    df['%D'] = df['%K'].rolling(window=params['stoch_d']).mean()

    # ATR
    df['TR'] = np.maximum(df['high'] - df['low'], 
                          np.maximum(abs(df['high'] - df['close'].shift()), 
                                     abs(df['low'] - df['close'].shift())))
    df['ATR'] = df['TR'].rolling(window=params['atr_period']).mean()

    console.log("[bold green]Semua indikator udah dihitung dengan sukses[/bold green]")
    return df.dropna().to_dict('records')
