# 🎮 Simulasi Agent-Based Modeling (ABM): Steam Support Refund Queue

Proyek ini mensimulasikan sistem antrean pengembalian dana (refund) pada layanan pelanggan menggunakan pendekatan **Agent-Based Modeling (ABM)**. Simulasi ini dibangun menggunakan **Mesa** sebagai mesin logika backend dan **Streamlit** sebagai antarmuka dashboard interaktif.

## 🌟 Deskripsi Proyek
Tujuan utama dari simulasi ini adalah untuk menganalisis dinamika operasional (panjang antrean dan waktu penyelesaian tiket) serta dampaknya terhadap kondisi psikologis pelanggan (tingkat frustrasi). Proyek ini juga dilengkapi dengan **Uji Monte Carlo** untuk mendapatkan rata-rata statistik yang valid dan menghilangkan bias dari nilai acak.

## ✨ Fitur Utama
* **Arsitektur Terpisah:** Menggunakan prinsip *Separation of Concerns* dengan memisahkan logika mesin (`model.py`) dan antarmuka visual (`app.py`).
* **Atribut Psikologis Agen:** Tiket pelanggan tidak hanya direpresentasikan sebagai angka, tetapi memiliki tingkat "Frustrasi" yang meningkat seiring lamanya waktu tunggu.
* **Visualisasi Real-Time:** Menampilkan grafik interaktif dari dinamika operasional dan psikologis pada satu putaran simulasi.
* **Uji Statistik Monte Carlo:** Mengeksekusi ratusan iterasi simulasi secara otomatis untuk mendapatkan rata-rata stabilitas sistem.
* **Skenario Intervensi (What-If):** * *Sistem Auto-Approval*: Menyetujui tiket secara otomatis jika memenuhi syarat tertentu.
  * *Dynamic Staffing*: Menambah staf secara otomatis ketika antrean mencapai batas kritis.

## 📂 Struktur Repositori
```text
├── app.py       # Tampilan antarmuka dashboard web (Frontend - Streamlit)
├── model.py     # Logika simulasi agen nasabah dan lingkungan (Backend - Mesa)
└── README.md    # Dokumentasi proyek

```

## 🛠️ Persyaratan Sistem (Dependencies)

Pastikan Anda telah menginstal Python di komputer Anda. Pustaka yang dibutuhkan untuk menjalankan proyek ini antara lain:

* `mesa`
* `streamlit`
* `matplotlib`
* `pandas`
* `numpy`

Anda dapat menginstal semua pustaka tersebut melalui terminal dengan perintah berikut:

```bash
pip install mesa streamlit matplotlib pandas numpy

```

## 🚀 Cara Menjalankan Proyek

1. *Clone* repositori ini ke dalam komputer Anda:
```bash
git clone [https://github.com/username-anda/nama-repo.git](https://github.com/username-anda/nama-repo.git)

```


2. Masuk ke dalam direktori proyek:
```bash
cd nama-repo

```


3. Jalankan aplikasi menggunakan Streamlit:
```bash
streamlit run app.py

```


4. Browser akan otomatis terbuka dan menampilkan Dashboard Simulasi (biasanya di `http://localhost:8501`).

## 📊 Tampilan Antarmuka

Dashboard terbagi menjadi dua *tab* utama:

1. **Visualisasi Simulasi Tunggal:** Mengatur parameter lewat *sidebar* dan melihat hasil dari satu kali skenario berjalan (Grafik Dinamika Operasional & Psikologis).
2. **Uji Monte Carlo:** Menjalankan skenario yang sama secara berulang-ulang (misal: 100-1000 kali) untuk melihat rata-rata hasil akhir secara analitik.

---

*Dibuat untuk keperluan Pemodelan dan Simulasi Data.*

```

```