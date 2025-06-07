import aiohttp
import json
from rich.console import Console
from trading_signals import signal_engine
import pandas as pd

console = Console()
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

async def analyze_with_gemini(data, api_key, symbol, timeframe):
    """Analisis menggunakan Gemini AI dengan data yang diperkaya"""
    console.log("[cyan]🤖 Memulai analisis AI dengan Gemini...[/cyan]")

    # Convert data to DataFrame for signal analysis
    df = pd.DataFrame(data)

    # Generate advanced trading signals
    trading_recommendation = signal_engine.generate_trading_recommendation(df, symbol, timeframe)

    headers = {
        "Content-Type": "application/json"
    }

    # Enhanced prompt with advanced analysis
    latest_data = data[-1] if data else {}
    previous_data = data[-2] if len(data) > 1 else {}

    prompt = f"""
    ANALISIS TRADING CRYPTOCURRENCY ADVANCED - {symbol} ({timeframe})

    🔍 DATA TEKNIKAL TERKINI:
    Current Price: ${latest_data.get('close', 'N/A')}
    RSI: {latest_data.get('RSI', 'N/A')}
    MACD: {latest_data.get('MACD', 'N/A')}
    Signal Score: {latest_data.get('Signal_Score', 'N/A')}
    Recommendation: {latest_data.get('Recommendation', 'N/A')}

    🤖 MACHINE LEARNING ANALYSIS:
    ML Signal: {trading_recommendation.get('ml_signal', 'N/A')}
    ML Confidence: {trading_recommendation.get('ml_confidence', 'N/A')}%
    Technical Score: {trading_recommendation.get('technical_score', 'N/A')}

    📊 ADVANCED INDICATORS:
    ADX: {latest_data.get('ADX', 'N/A')}
    Williams %R: {latest_data.get('Williams_R', 'N/A')}
    CCI: {latest_data.get('CCI', 'N/A')}
    Trend Strength: {latest_data.get('Trend_Strength', 'N/A')}

    🎯 TRADING RECOMMENDATION SYSTEM:
    Action: {trading_recommendation.get('action', 'N/A')}
    Confidence: {trading_recommendation.get('confidence', 'N/A')}%
    Entry Price: ${trading_recommendation.get('entry_price', 'N/A')}
    Stop Loss: ${trading_recommendation.get('stop_loss', 'N/A')}
    Take Profit 1: ${trading_recommendation.get('take_profit_1', 'N/A')}
    Take Profit 2: ${trading_recommendation.get('take_profit_2', 'N/A')}
    Risk/Reward: {trading_recommendation.get('risk_reward_ratio', 'N/A')}

    📈 SUPPORT/RESISTANCE:
    Support: ${trading_recommendation.get('support', 'N/A')}
    Resistance: ${trading_recommendation.get('resistance', 'N/A')}

    ⚡ VOLATILITY & RISK:
    Volatility: {trading_recommendation.get('volatility', 'N/A')}%
    ATR%: {trading_recommendation.get('atr_percent', 'N/A')}%

    🔥 CANDLESTICK PATTERNS:
    Doji: {latest_data.get('Doji', False)}
    Hammer: {latest_data.get('Hammer', False)}
    Shooting Star: {latest_data.get('Shooting_Star', False)}
    Bullish Engulfing: {latest_data.get('Bullish_Engulfing', False)}
    Bearish Engulfing: {latest_data.get('Bearish_Engulfing', False)}

    Berdasarkan analisis teknikal advanced dan machine learning di atas, berikan analisis mendalam dengan format:

    🎯 EXECUTIVE SUMMARY:
    [Ringkasan singkat kondisi pasar dan rekomendasi utama]

    📊 ANALISIS TEKNIKAL MENDALAM:
    1. Trend Analysis: [Analisis trend multi-timeframe]
    2. Momentum Indicators: [RSI, MACD, Stochastic analysis]
    3. Volatility Analysis: [Bollinger Bands, ATR analysis]
    4. Volume Analysis: [Volume patterns dan VWAP]
    5. Advanced Indicators: [ADX, CCI, Williams %R]

    🤖 MACHINE LEARNING INSIGHTS:
    [Interpretasi hasil ML dan confidence level]

    🎯 TRADING STRATEGY:
    - Entry Strategy: [Kapan dan bagaimana masuk]
    - Exit Strategy: [Target profit dan stop loss]
    - Position Sizing: [Berapa % portfolio untuk trade ini]
    - Risk Management: [Strategi manajemen risiko]

    ⚠️ RISK ASSESSMENT:
    - Risk Level: [Low/Medium/High]
    - Key Risks: [Faktor risiko utama]
    - Market Conditions: [Kondisi pasar saat ini]

    🔮 MARKET OUTLOOK:
    [Prediksi pergerakan harga jangka pendek dan menengah]

    💡 TRADING TIPS:
    [Tips praktis untuk eksekusi trading]

    Berikan analisis yang objektif, data-driven, dan actionable!
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
