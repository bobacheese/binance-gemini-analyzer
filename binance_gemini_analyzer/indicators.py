import numpy as np
import pandas as pd
from rich.console import Console
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

console = Console()

def get_indicator_params(timeframe):
    if timeframe in ['1m', '5m']:
        return {
            'sma_fast': 10, 'sma_slow': 30, 'sma_long': 50,
            'ema_fast': 6, 'ema_slow': 13, 'ema_long': 21,
            'rsi_period': 7, 'rsi_overbought': 75, 'rsi_oversold': 25,
            'bb_period': 10, 'bb_std': 2,
            'macd_fast': 6, 'macd_slow': 13, 'macd_signal': 4,
            'stoch_k': 5, 'stoch_d': 3, 'stoch_overbought': 80, 'stoch_oversold': 20,
            'atr_period': 7, 'adx_period': 7, 'cci_period': 10,
            'williams_period': 7, 'vwap_period': 20,
            'ichimoku_tenkan': 4, 'ichimoku_kijun': 13, 'ichimoku_senkou': 26
        }
    elif timeframe in ['15m', '30m', '1h']:
        return {
            'sma_fast': 20, 'sma_slow': 50, 'sma_long': 100,
            'ema_fast': 12, 'ema_slow': 26, 'ema_long': 50,
            'rsi_period': 14, 'rsi_overbought': 70, 'rsi_oversold': 30,
            'bb_period': 20, 'bb_std': 2,
            'macd_fast': 12, 'macd_slow': 26, 'macd_signal': 9,
            'stoch_k': 14, 'stoch_d': 3, 'stoch_overbought': 80, 'stoch_oversold': 20,
            'atr_period': 14, 'adx_period': 14, 'cci_period': 20,
            'williams_period': 14, 'vwap_period': 50,
            'ichimoku_tenkan': 9, 'ichimoku_kijun': 26, 'ichimoku_senkou': 52
        }
    else:  # 4h, 1d
        return {
            'sma_fast': 50, 'sma_slow': 200, 'sma_long': 300,
            'ema_fast': 21, 'ema_slow': 55, 'ema_long': 100,
            'rsi_period': 21, 'rsi_overbought': 65, 'rsi_oversold': 35,
            'bb_period': 50, 'bb_std': 2,
            'macd_fast': 21, 'macd_slow': 55, 'macd_signal': 13,
            'stoch_k': 21, 'stoch_d': 7, 'stoch_overbought': 75, 'stoch_oversold': 25,
            'atr_period': 21, 'adx_period': 21, 'cci_period': 30,
            'williams_period': 21, 'vwap_period': 100,
            'ichimoku_tenkan': 20, 'ichimoku_kijun': 60, 'ichimoku_senkou': 120
        }

def calculate_advanced_indicators(df, params):
    """Menghitung indikator teknikal advanced"""
    console.log("[cyan]Menghitung indikator advanced...[/cyan]")

    # Williams %R
    df['Williams_R'] = ((df['high'].rolling(window=params['williams_period']).max() - df['close']) /
                       (df['high'].rolling(window=params['williams_period']).max() -
                        df['low'].rolling(window=params['williams_period']).min())) * -100

    # Commodity Channel Index (CCI)
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    sma_tp = typical_price.rolling(window=params['cci_period']).mean()
    mad = typical_price.rolling(window=params['cci_period']).apply(lambda x: np.mean(np.abs(x - x.mean())))
    df['CCI'] = (typical_price - sma_tp) / (0.015 * mad)

    # Average Directional Index (ADX)
    high_diff = df['high'].diff()
    low_diff = df['low'].diff()
    plus_dm = np.where((high_diff > low_diff) & (high_diff > 0), high_diff, 0)
    minus_dm = np.where((low_diff > high_diff) & (low_diff > 0), low_diff, 0)

    tr = np.maximum(df['high'] - df['low'],
                    np.maximum(abs(df['high'] - df['close'].shift()),
                              abs(df['low'] - df['close'].shift())))

    plus_di = 100 * (pd.Series(plus_dm).rolling(window=params['adx_period']).mean() /
                     pd.Series(tr).rolling(window=params['adx_period']).mean())
    minus_di = 100 * (pd.Series(minus_dm).rolling(window=params['adx_period']).mean() /
                      pd.Series(tr).rolling(window=params['adx_period']).mean())

    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    df['ADX'] = dx.rolling(window=params['adx_period']).mean()
    df['Plus_DI'] = plus_di
    df['Minus_DI'] = minus_di

    # VWAP (Volume Weighted Average Price)
    df['VWAP'] = (df['close'] * df['volume']).rolling(window=params['vwap_period']).sum() / df['volume'].rolling(window=params['vwap_period']).sum()

    return df

def calculate_ichimoku(df, params):
    """Menghitung Ichimoku Cloud"""
    console.log("[cyan]Menghitung Ichimoku Cloud...[/cyan]")

    # Tenkan-sen (Conversion Line)
    tenkan_high = df['high'].rolling(window=params['ichimoku_tenkan']).max()
    tenkan_low = df['low'].rolling(window=params['ichimoku_tenkan']).min()
    df['Tenkan_sen'] = (tenkan_high + tenkan_low) / 2

    # Kijun-sen (Base Line)
    kijun_high = df['high'].rolling(window=params['ichimoku_kijun']).max()
    kijun_low = df['low'].rolling(window=params['ichimoku_kijun']).min()
    df['Kijun_sen'] = (kijun_high + kijun_low) / 2

    # Senkou Span A (Leading Span A)
    df['Senkou_A'] = ((df['Tenkan_sen'] + df['Kijun_sen']) / 2).shift(params['ichimoku_kijun'])

    # Senkou Span B (Leading Span B)
    senkou_high = df['high'].rolling(window=params['ichimoku_senkou']).max()
    senkou_low = df['low'].rolling(window=params['ichimoku_senkou']).min()
    df['Senkou_B'] = ((senkou_high + senkou_low) / 2).shift(params['ichimoku_kijun'])

    # Chikou Span (Lagging Span)
    df['Chikou_span'] = df['close'].shift(-params['ichimoku_kijun'])

    return df

def detect_candlestick_patterns(df):
    """Mendeteksi pola candlestick"""
    console.log("[cyan]Mendeteksi pola candlestick...[/cyan]")

    # Doji
    body_size = abs(df['close'] - df['open'])
    total_range = df['high'] - df['low']
    df['Doji'] = (body_size / total_range < 0.1) & (total_range > 0)

    # Hammer
    lower_shadow = np.where(df['close'] > df['open'], df['open'] - df['low'], df['close'] - df['low'])
    upper_shadow = np.where(df['close'] > df['open'], df['high'] - df['close'], df['high'] - df['open'])
    df['Hammer'] = (lower_shadow > 2 * body_size) & (upper_shadow < body_size) & (body_size > 0)

    # Shooting Star
    df['Shooting_Star'] = (upper_shadow > 2 * body_size) & (lower_shadow < body_size) & (body_size > 0)

    # Engulfing Patterns
    df['Bullish_Engulfing'] = ((df['close'].shift(1) < df['open'].shift(1)) &
                               (df['close'] > df['open']) &
                               (df['open'] < df['close'].shift(1)) &
                               (df['close'] > df['open'].shift(1)))

    df['Bearish_Engulfing'] = ((df['close'].shift(1) > df['open'].shift(1)) &
                               (df['close'] < df['open']) &
                               (df['open'] > df['close'].shift(1)) &
                               (df['close'] < df['open'].shift(1)))

    return df

def calculate_support_resistance(df, window=20):
    """Menghitung level support dan resistance"""
    console.log("[cyan]Menghitung support/resistance...[/cyan]")

    # Local maxima dan minima
    df['Local_Max'] = df['high'].rolling(window=window, center=True).max() == df['high']
    df['Local_Min'] = df['low'].rolling(window=window, center=True).min() == df['low']

    # Resistance levels
    resistance_levels = df[df['Local_Max']]['high'].tail(5).tolist()
    df['Resistance_1'] = max(resistance_levels) if resistance_levels else df['high'].max()
    df['Resistance_2'] = sorted(resistance_levels, reverse=True)[1] if len(resistance_levels) > 1 else df['Resistance_1']

    # Support levels
    support_levels = df[df['Local_Min']]['low'].tail(5).tolist()
    df['Support_1'] = min(support_levels) if support_levels else df['low'].min()
    df['Support_2'] = sorted(support_levels)[1] if len(support_levels) > 1 else df['Support_1']

    return df

def calculate_trend_strength(df):
    """Menghitung kekuatan trend"""
    console.log("[cyan]Menghitung kekuatan trend...[/cyan]")

    # Linear regression untuk trend
    x = np.arange(len(df))
    y = df['close'].values

    if len(y) > 1:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        df['Trend_Slope'] = slope
        df['Trend_R2'] = r_value ** 2
        df['Trend_Strength'] = abs(slope) * (r_value ** 2)  # Kombinasi slope dan R²
    else:
        df['Trend_Slope'] = 0
        df['Trend_R2'] = 0
        df['Trend_Strength'] = 0

    # Moving average trend
    df['MA_Trend'] = np.where(df['close'] > df['close'].rolling(20).mean(), 1, -1)

    return df

def calculate_signal_score(df, params):
    """Menghitung skor sinyal trading berdasarkan multiple indikator"""
    console.log("[cyan]Menghitung skor sinyal trading...[/cyan]")

    df['Signal_Score'] = 0
    df['Buy_Signals'] = 0
    df['Sell_Signals'] = 0

    # RSI Signals
    df.loc[df['RSI'] < params['rsi_oversold'], 'Buy_Signals'] += 1
    df.loc[df['RSI'] > params['rsi_overbought'], 'Sell_Signals'] += 1

    # MACD Signals
    df.loc[(df['MACD'] > df['MACD_Signal']) & (df['MACD'].shift(1) <= df['MACD_Signal'].shift(1)), 'Buy_Signals'] += 2
    df.loc[(df['MACD'] < df['MACD_Signal']) & (df['MACD'].shift(1) >= df['MACD_Signal'].shift(1)), 'Sell_Signals'] += 2

    # Stochastic Signals
    df.loc[(df['%K'] < params['stoch_oversold']) & (df['%K'] > df['%D']), 'Buy_Signals'] += 1
    df.loc[(df['%K'] > params['stoch_overbought']) & (df['%K'] < df['%D']), 'Sell_Signals'] += 1

    # Moving Average Signals
    ma_fast_col = f'EMA_{params["ema_fast"]}'
    ma_slow_col = f'EMA_{params["ema_slow"]}'
    df.loc[(df[ma_fast_col] > df[ma_slow_col]) & (df[ma_fast_col].shift(1) <= df[ma_slow_col].shift(1)), 'Buy_Signals'] += 2
    df.loc[(df[ma_fast_col] < df[ma_slow_col]) & (df[ma_fast_col].shift(1) >= df[ma_slow_col].shift(1)), 'Sell_Signals'] += 2

    # Bollinger Bands Signals
    df.loc[df['close'] < df['BB_Lower'], 'Buy_Signals'] += 1
    df.loc[df['close'] > df['BB_Upper'], 'Sell_Signals'] += 1

    # Williams %R Signals
    df.loc[df['Williams_R'] < -80, 'Buy_Signals'] += 1
    df.loc[df['Williams_R'] > -20, 'Sell_Signals'] += 1

    # ADX Trend Strength
    strong_trend = df['ADX'] > 25
    df.loc[strong_trend & (df['Plus_DI'] > df['Minus_DI']), 'Buy_Signals'] += 1
    df.loc[strong_trend & (df['Plus_DI'] < df['Minus_DI']), 'Sell_Signals'] += 1

    # Candlestick Pattern Signals
    df.loc[df['Hammer'] | df['Bullish_Engulfing'], 'Buy_Signals'] += 1
    df.loc[df['Shooting_Star'] | df['Bearish_Engulfing'], 'Sell_Signals'] += 1

    # Final Signal Score (-10 to +10)
    df['Signal_Score'] = df['Buy_Signals'] - df['Sell_Signals']
    df['Signal_Score'] = np.clip(df['Signal_Score'], -10, 10)

    # Signal Strength
    df['Signal_Strength'] = abs(df['Signal_Score']) / 10 * 100  # Percentage

    # Trading Recommendation
    df['Recommendation'] = 'HOLD'
    df.loc[df['Signal_Score'] >= 3, 'Recommendation'] = 'STRONG_BUY'
    df.loc[df['Signal_Score'] == 2, 'Recommendation'] = 'BUY'
    df.loc[df['Signal_Score'] == 1, 'Recommendation'] = 'WEAK_BUY'
    df.loc[df['Signal_Score'] == -1, 'Recommendation'] = 'WEAK_SELL'
    df.loc[df['Signal_Score'] == -2, 'Recommendation'] = 'SELL'
    df.loc[df['Signal_Score'] <= -3, 'Recommendation'] = 'STRONG_SELL'

    return df

def calculate_indicators(klines, timeframe):
    """Fungsi utama untuk menghitung semua indikator teknikal"""
    console.log("[bold green]🚀 Memulai analisis teknikal advanced...[/bold green]")

    params = get_indicator_params(timeframe)

    # Konversi data ke DataFrame
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])

    # Konversi tipe data
    numeric_columns = ['open', 'high', 'low', 'close', 'volume']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    console.log("[green]✅ Data berhasil dikonversi[/green]")

    # Indikator Dasar
    console.log("[cyan]📊 Menghitung indikator dasar...[/cyan]")

    # Simple Moving Averages
    df[f'SMA_{params["sma_fast"]}'] = df['close'].rolling(window=params['sma_fast']).mean()
    df[f'SMA_{params["sma_slow"]}'] = df['close'].rolling(window=params['sma_slow']).mean()
    df[f'SMA_{params["sma_long"]}'] = df['close'].rolling(window=params['sma_long']).mean()

    # Exponential Moving Averages
    df[f'EMA_{params["ema_fast"]}'] = df['close'].ewm(span=params['ema_fast'], adjust=False).mean()
    df[f'EMA_{params["ema_slow"]}'] = df['close'].ewm(span=params['ema_slow'], adjust=False).mean()
    df[f'EMA_{params["ema_long"]}'] = df['close'].ewm(span=params['ema_long'], adjust=False).mean()

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
    df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Middle'] * 100

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
    df['ATR_Percent'] = (df['ATR'] / df['close']) * 100

    # Indikator Advanced
    df = calculate_advanced_indicators(df, params)
    df = calculate_ichimoku(df, params)
    df = detect_candlestick_patterns(df)
    df = calculate_support_resistance(df)
    df = calculate_trend_strength(df)
    df = calculate_signal_score(df, params)

    console.log("[bold green]🎯 Semua indikator berhasil dihitung![/bold green]")
    console.log(f"[yellow]📈 Total data points: {len(df)}[/yellow]")
    console.log(f"[yellow]🔍 Sinyal terakhir: {df['Recommendation'].iloc[-1] if not df.empty else 'N/A'}[/yellow]")

    # Fill NaN values instead of dropping them
    df = df.fillna(0)

    # Only return data where we have enough for meaningful analysis
    min_periods = max(params.get('sma_slow', 50), params.get('bb_period', 20))
    if len(df) > min_periods:
        return df.iloc[min_periods:].to_dict('records')
    else:
        return df.to_dict('records')
