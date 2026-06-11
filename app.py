import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from model import SteamSupportModel

st.set_page_config(page_title="Simulasi Steam Support", layout="wide")

st.title("Simulasi Antrean Refund Request Steam Support")
st.markdown("Proyek Pemodelan dan Simulasi Data dengan Agent-Based Modeling (ABM) & Uji Monte Carlo")

st.sidebar.header("Konfigurasi Parameter Skenario")
steps = st.sidebar.slider("Lama Waktu Simulasi (Ticks)", min_value=10, max_value=200, value=100)
base_staff = st.sidebar.number_input("Jumlah Staf Reguler", min_value=1, max_value=10, value=3)
max_arrival = st.sidebar.slider("Maksimal Tiket Masuk per Tick (Stressor)", min_value=1, max_value=20, value=4)

st.sidebar.subheader("Pengaturan Intervensi (Skenario)")
auto_approval = st.sidebar.checkbox("1. Sistem Auto-Approval Aktif")
dynamic_staffing = st.sidebar.checkbox("2. Sistem Dynamic Staffing Aktif")

q_threshold = 10
extra_staff = 2
if dynamic_staffing:
    q_threshold = st.sidebar.number_input("Batas Antrean Pemicu (Threshold)", min_value=5, value=10)
    extra_staff = st.sidebar.number_input("Jumlah Staf Tambahan", min_value=1, value=2)

st.sidebar.markdown("---")

tab1, tab2 = st.tabs(["📊 Visualisasi Simulasi Tunggal", "🔄 Uji Monte Carlo (Multi-Iterasi)"])

with tab1:
    st.header("Visualisasi Real-Time (1 Putaran)")
    st.markdown("Tab ini berguna untuk melihat dinamika pergerakan antrean dan frustrasi pelanggan pada satu kali skenario berjalan.")
    
    if st.button("Jalankan Simulasi Tunggal", type="primary"):
        model = SteamSupportModel(base_staff, auto_approval, dynamic_staffing, q_threshold, extra_staff, max_arrival)
        for i in range(steps):
            model.step()
            
        results = model.datacollector.get_model_vars_dataframe()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Tiket Diselesaikan", results["Tiket_Selesai"].iloc[-1])
        col2.metric("Puncak Antrean", results["Panjang_Antrean"].max())
        col3.metric("Staf Aktif Terakhir", results["Total_Staf"].iloc[-1])
        col4.metric("Rata-rata Frustrasi (0-1)", round(results["Rata_Rata_Frustrasi"].iloc[-1], 3))
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        ax1.plot(results.index, results["Panjang_Antrean"], label="Panjang Antrean", color="red")
        ax1.plot(results.index, results["Tiket_Selesai"], label="Tiket Selesai", color="green")
        ax1.set_title("Dinamika Operasional (Antrean vs Selesai)")
        ax1.set_ylabel("Jumlah Tiket")
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(results.index, results["Rata_Rata_Frustrasi"], label="Tingkat Frustrasi Pelanggan", color="purple", linewidth=2)
        ax2.set_title("Dampak Keterlambatan Terhadap Psikologis Pelanggan")
        ax2.set_xlabel("Waktu Simulasi (Ticks)")
        ax2.set_ylabel("Skala Frustrasi (0.0 - 1.0)")
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        st.pyplot(fig)

with tab2:
    st.header("Uji Monte Carlo (Evaluasi Statistik)")
    st.markdown("Tab ini digunakan untuk memenuhi standar akademis dengan menjalankan simulasi ratusan kali guna mendapatkan rata-rata statistik yang valid (menghilangkan bias nilai acak).")
    
    num_iterations = st.slider("Jumlah Iterasi (Runs)", min_value=10, max_value=1000, value=100, step=10)
    
    if st.button("Jalankan Uji Monte Carlo"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        mc_results = []
        
        for i in range(num_iterations):
            if i % 10 == 0 or i == num_iterations - 1:
                progress_bar.progress((i + 1) / num_iterations)
                status_text.text(f"Menjalankan iterasi {i+1} dari {num_iterations}...")
                
            model = SteamSupportModel(base_staff, auto_approval, dynamic_staffing, q_threshold, extra_staff, max_arrival)
            for _ in range(steps):
                model.step()
                
            df = model.datacollector.get_model_vars_dataframe()
            mc_results.append({
                "Puncak Antrean": df["Panjang_Antrean"].max(),
                "Total Tiket Selesai": df["Tiket_Selesai"].iloc[-1],
                "Rata-rata Frustrasi Akhir": df["Rata_Rata_Frustrasi"].iloc[-1]
            })
            
        status_text.text("Simulasi Monte Carlo Selesai!")
        
        df_mc = pd.DataFrame(mc_results)
        
        st.subheader(f"Hasil Rata-Rata dari {num_iterations} Iterasi")
        mcol1, mcol2, mcol3 = st.columns(3)
        mcol1.metric("Rata-rata Puncak Antrean", round(df_mc["Puncak Antrean"].mean(), 1))
        mcol2.metric("Rata-rata Tiket Selesai", round(df_mc["Total Tiket Selesai"].mean(), 1))
        mcol3.metric("Rata-rata Frustrasi (0-1)", round(df_mc["Rata-rata Frustrasi Akhir"].mean(), 3))
        
        st.markdown("---")
        st.write("**Distribusi Data Mentah (5 Sampel Pertama):**")
        st.dataframe(df_mc.head())