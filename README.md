# 🚀 Binance Gemini Analyzer v2.0 Enhanced

Binance Gemini Analyzer adalah alat trading cryptocurrency paling canggih yang menggabungkan 15+ indikator teknikal advanced, machine learning, dan AI analysis untuk menghasilkan sinyal trading yang akurat dan profitable.

## 🎯 Fitur Utama v2.0

### 🤖 **Advanced AI & Machine Learning**
- **15+ Indikator Teknikal**: RSI, MACD, ADX, Williams %R, CCI, Ichimoku Cloud, VWAP, dll
- **Machine Learning Engine**: Random Forest untuk prediksi sinyal dengan confidence scoring
- **Pattern Recognition**: Deteksi otomatis candlestick patterns (Doji, Hammer, Engulfing, dll)
- **AI-Powered Analysis**: Analisis mendalam menggunakan Gemini AI dengan prompt yang disempurnakan

### 📊 **Advanced Technical Analysis**
- **Multi-Indicator Scoring**: Sistem scoring gabungan dari semua indikator (-10 to +10)
- **Support/Resistance Detection**: Deteksi otomatis level support dan resistance
- **Trend Strength Analysis**: Pengukuran kekuatan trend dengan linear regression
- **Volatility Analysis**: ATR percentage dan volatility measurement real-time

### ⚡ **Smart Trading Signals**
- **Signal Confidence**: Tingkat kepercayaan sinyal (0-100%)
- **Risk/Reward Calculation**: Kalkulasi otomatis R:R ratio
- **Position Sizing**: Rekomendasi ukuran posisi berdasarkan risk
- **Multi-timeframe Confirmation**: Analisis konfirmasi di berbagai timeframe

### 🛡️ **Advanced Risk Management**
- **ATR-based Stop Loss**: Stop loss dinamis berdasarkan volatility
- **Dynamic Take Profit**: Multiple take profit levels
- **Risk Metrics**: Comprehensive risk analysis dan monitoring
- **Market Condition Detection**: Identifikasi kondisi Bull/Bear/Sideways

### 🖥️ **Enhanced User Experience**
- **Trading Dashboard**: Interface komprehensif dengan semua informasi penting
- **Real-time Updates**: Data dan sinyal terupdate secara real-time
- **Color-coded Signals**: Visual indicators yang mudah dipahami
- **Cross-platform**: Desktop, mobile, dan Termux support

## 🛠️ Instalasi

### Prasyarat

- Python 3.7+
- pip
- git

### Langkah-langkah Instalasi

1. **Clone Repository**
   ```bash
   git clone https://github.com/username-lo/binance-gemini-analyzer.git
   cd binance-gemini-analyzer
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Unix atau MacOS
   # atau
   .\venv\Scripts\activate  # Untuk Windows
   ```

3. **Install Dependencies**
   ```bash
   cd binance_gemini_analyzer
   pip install -r requirements.txt
   ```

4. **Konfigurasi API Key**
   Set environment variable atau edit `config.py`:
   ```bash
   export GEMINI_API_KEY="API_KEY_LO_DISINI"
   ```
   Atau edit file `config.py`:
   ```python
   GEMINI_API_KEY = "API_KEY_LO_DISINI"
   ```

## 🖥️ Cara Penggunaan

1. Aktifkan virtual environment (jika belum):
   ```bash
   source venv/bin/activate  # Untuk Unix atau MacOS
   # atau
   .\venv\Scripts\activate  # Untuk Windows
   ```

2. Jalankan program:
   ```bash
   cd binance_gemini_analyzer
   python main.py
   ```

3. **Test dengan Data Simulasi** (jika Binance tidak accessible):
   ```bash
   python test_with_simulation.py
   ```

4. Ikuti petunjuk di layar:
   - Masukkan pair cryptocurrency (contoh: BTCUSDT)
   - Pilih timeframe (1m, 5m, 15m, 1h, 4h, 1d)
   - Lihat dashboard trading yang komprehensif

5. Analisis hasil:
   - **Trading Signals**: Action, confidence, entry/exit points
   - **Risk Metrics**: Stop loss, take profit, R:R ratio
   - **Technical Indicators**: 15+ indikator dengan scoring
   - **ML Analysis**: Prediksi machine learning dengan confidence
   - **AI Insights**: Analisis mendalam dari Gemini AI

## 📱 Instalasi di Termux

1. Update Termux:
   ```bash
   pkg update && pkg upgrade -y
   ```

2. Install dependencies:
   ```bash
   pkg install python git
   ```

3. Ikuti langkah 1-4 dari [Langkah-langkah Instalasi](#langkah-langkah-instalasi) di atas

## 🎯 Fitur Advanced v2.0

### 📊 **Indikator Teknikal Lengkap**
| Indikator | Fungsi | Timeframe Support |
|-----------|--------|-------------------|
| RSI | Momentum oscillator | Adaptive threshold |
| MACD | Trend following | Multi-timeframe |
| ADX | Trend strength | Dynamic calculation |
| Williams %R | Overbought/oversold | All timeframes |
| CCI | Commodity Channel Index | Deviation analysis |
| Bollinger Bands | Volatility bands | Width analysis |
| Stochastic | Momentum oscillator | Adaptive levels |
| VWAP | Volume weighted price | Real-time |
| Ichimoku Cloud | Complete system | 5 components |
| ATR | Volatility measure | Percentage based |

### 🤖 **Machine Learning Features**
- **Random Forest Classifier**: Prediksi sinyal dengan akurasi tinggi
- **Feature Engineering**: 12+ fitur teknikal untuk training
- **Confidence Scoring**: Tingkat kepercayaan 0-100%
- **Auto-training**: Model ditraining otomatis dengan data historis

### 🕯️ **Pattern Recognition**
- **Doji**: Market indecision
- **Hammer**: Bullish reversal
- **Shooting Star**: Bearish reversal
- **Bullish Engulfing**: Strong buy signal
- **Bearish Engulfing**: Strong sell signal

### 🎯 **Smart Signal System**
```
Signal Score Range: -10 to +10
- STRONG_BUY: Score ≥ 3
- BUY: Score = 2
- WEAK_BUY: Score = 1
- HOLD: Score = 0
- WEAK_SELL: Score = -1
- SELL: Score = -2
- STRONG_SELL: Score ≤ -3
```

### 🛡️ **Risk Management**
- **ATR-based Stop Loss**: Dinamis berdasarkan volatility
- **Multiple Take Profit**: 2 level target profit
- **Position Sizing**: Berdasarkan risk tolerance
- **R:R Calculation**: Risk/Reward ratio otomatis

## 🔧 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| ModuleNotFoundError | Coba install ulang dependencies: `pip install -r requirements.txt` |
| Koneksi Error | Periksa koneksi internet Anda |
| Gemini API Error | Pastikan API key di `config.py` sudah benar |
| Layar Penuh | Perbesar font Termux atau putar device ke mode landscape |

## 🤝 Kontribusi

Kami sangat menghargai kontribusi dari komunitas. Jika Anda punya ide untuk meningkatkan tool ini:

1. Fork repository ini
2. Buat branch baru 
3. Commit perubahan Anda
4. Push ke branch
5. Buat Pull Request baru

## 📜 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file [LICENSE](LICENSE) untuk detailnya.

## 📞 Kontak

Punya pertanyaan? Hubungi kami di bagian issue.

---

<p align="center">
  Dibuat oleh bobacheese
  <br>
  <a href="https://www.buymeacoffee.com/bobacheese">
    <img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee">
  </a>
</p>
