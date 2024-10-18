# 🚀 Binance Gemini Analyzer

Binance Gemini Analyzer adalah alat canggih untuk analisis trading cryptocurrency yang menggabungkan kekuatan data real-time dari Binance dengan kecerdasan buatan Gemini. Cocok buat trader pemula maupun yang udah pro.

## 📊 Fitur Utama

- **Real-time Analysis**: Dapatkan data terkini langsung dari Binance
- **AI-Powered Insights**: Analisis mendalam menggunakan Gemini AI
- **Multi-timeframe Support**: Analisis berbagai timeframe dari 1 menit hingga 1 hari
- **User-friendly Interface**: Tampilan keren dan mudah digunakan berkat library blessed
- **Cross-platform**: Bisa dijalankan di desktop atau di smartphone via Termux

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
   pip install -r requirements.txt
   ```

4. **Konfigurasi API Key**
   Buat file `config.py` di root folder dan isi dengan:
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
   python main.py
   ```

3. Ikuti petunjuk di layar:
   - Masukkan pair cryptocurrency (contoh: BTCUSDT)
   - Pilih timeframe (1m, 5m, 15m, 1h, 4h, 1d)

4. Tunggu analisis selesai dan baca hasilnya dengan seksama

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
