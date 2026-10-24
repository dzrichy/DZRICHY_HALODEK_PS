import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# ---------------------------------------------------------
# KONFIGURASI HALAMAN STREAMLIT
# ---------------------------------------------------------
st.set_page_config(
    page_title="OptiHealth - Sistem Antrean & Triage Telemedis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan lebih modern
st.markdown(""")
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2563EB;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER UTAMA
# ---------------------------------------------------------
st.markdown('<p class="main-header">🏥 OptiHealth - Telemedicine Queue & Triage System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Aplikasi Solusi Antrean & Efisiensi Layanan Kesehatan berbasis Teknik Industri</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR / NAVIGASI SISTEM
# ---------------------------------------------------------
st.sidebar.title("📌 Menu Navigasi")
menu = st.sidebar.radio(
    "Pilih Modul Aplikasi:",
    ["1. Registrasi & Pre-Triage Pasien", "2. Monitor Antrean & Estimasi Waktu", "3. Dashboard Analisis Performa (TI)"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Konteks Teknik Industri:**
Aplikasi ini dikembangkan untuk mengoptimalkan *Queue Management*, mereduksi *Idle Time* dokter, dan mempercepat alur informasi (*Information Flow*) sebelum konsultasi dimulai.
""")

# Initial State / Database Sederhana dalam Memory
if 'queue_data' not in st.session_state:
    st.session_state['queue_data'] = [
        {"ID": "P001", "Nama": "Budi Santoso", "Dokter": "dr. Andi (Sp.PD)", "Triase": "Sedang", "Waktu Tunggu (m)": 10},
        {"ID": "P002", "Nama": "Siti Rahma", "Dokter": "dr. Rina (Umum)", "Triase": "Ringan", "Waktu Tunggu (m)": 5},
        {"ID": "P003", "Nama": "Ahmad Fauzi", "Dokter": "dr. Andi (Sp.PD)", "Triase": "Berat", "Waktu Tunggu (m)": 25},
    ]

# ---------------------------------------------------------
# MODUL 1: REGISTRASI & PRE-TRIAGE
# ---------------------------------------------------------
if menu == "1. Registrasi & Pre-Triage Pasien":
    st.header("📋 Registrasi Pasien & Pre-Triage Diagnosa")
    st.write("Isi formulir ini untuk mempercepat durasi konsultasi dokter (*Waste Reduction*).")

    col1, col2 = st.columns(2)

    with col1:
        nama = st.text_input("Nama Lengkap Pasien")
        usia = st.number_input("Usia (Tahun)", min_value=1, max_value=100, value=22)
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        dokter = st.selectbox("Pilih Dokter Spasialis/Umum", [
            "dr. Andi, Sp.PD (Penyakit Dalam)",
            "dr. Rina (Dokter Umum)",
            "dr. Maya, Sp.A (Anak)"
        ])

    with col2:
        keluhan = st.text_area("Keluhan Utama / Gejala", placeholder="Contoh: Demam 3 hari, pusing, dan mual...")
        tingkat_keparahan = st.select_slider(
            "Tingkat Keparahan Gejala (Self-Triage)",
            options=["Ringan", "Sedang", "Berat"]
        )
        sistolik = st.number_input("Tekanan Darah Sistolik (opsional)", value=120)

    if st.button("🔴 Daftarkan & Masuk Antrean"):
        if nama and keluhan:
            # Hitung estimasi waktu
            est_time = 15 if tingkat_keparahan == "Ringan" else (25 if tingkat_keparahan == "Sedang" else 35)
            
            # Tambahkan data
            new_id = f"P00{len(st.session_state['queue_data']) + 1}"
            st.session_state['queue_data'].append({
                "ID": new_id,
                "Nama": nama,
                "Dokter": dokter,
                "Triase": tingkat_keparahan,
                "Waktu Tunggu (m)": est_time
            })
            
            st.success(f"Berhasil Mendaftar! Nomor Antrean Anda: **{new_id}**")
            st.info(f"Estimasi Waktu Tunggu Layanan: **± {est_time} Menit**")
        else:
            st.warning("Mohon isi Nama dan Keluhan Utama terlebih dahulu.")

# ---------------------------------------------------------
# MODUL 2: MONITOR ANTREAN
# ---------------------------------------------------------
elif menu == "2. Monitor Antrean & Estimasi Waktu":
    st.header("⏳ Monitor Antrean & Estimasi Waktu Real-Time")
    
    df_queue = pd.DataFrame(st.session_state['queue_data'])

    # Top Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Pasien dalam Antrean", len(df_queue))
    c2.metric("Rata-Rata Waktu Tunggu", f"{df_queue['Waktu Tunggu (m)'].mean():.1f} Menit")
    c3.metric("Status Server Telemedis", "Normal (Optimal)")

    st.subheader("Daftar Antrean Aktif")
    st.dataframe(df_queue, use_container_width=True)

    st.subheader("💡 Simulasi Antrean Menurut Dokter")
    dokter_selected = st.selectbox("Pilih Dokter untuk Melihat Alur Antrean", df_queue["Dokter"].unique())
    df_filtered = df_queue[df_queue["Dokter"] == dokter_selected]

    st.write(f"Antrean Spesifik untuk **{dokter_selected}**:")
    st.table(df_filtered[["ID", "Nama", "Triase", "Waktu Tunggu (m)"]])

# ---------------------------------------------------------
# MODUL 3: DASHBOARD ANALISIS TEKNIK INDUSTRI
# ---------------------------------------------------------
elif menu == "3. Dashboard Analisis Performa (TI)":
    st.header("📊 Dashboard Analisis Kinerja Sistem (Teknik Industri)")

    st.markdown("""
    **Indikator Kinerja Utama (*KPIs*):**
    * **Throughput Time:** Menurunkan rata-rata durasi konsultasi dengan sistem pre-triage.
    * **Resource Utilization:** Optimasi tingkat penggunaan kapasitas waktu dokter.
    """)

    # Generate Dummy Data untuk Analisis Grafik
    np.random.seed(42)
    hours = [f"{h:02d}:00" for h in range(8, 18)]
    pasien_masuk = np.random.randint(5, 25, size=len(hours))
    waktu_tunggu_avg = np.random.randint(10, 45, size=len(hours))

    df_analytics = pd.DataFrame({
        "Jam Operational": hours,
        "Jumlah Pasien": pasien_masuk,
        "Rata-rata Waktu Tunggu (Menit)": waktu_tunggu_avg
    })

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Beban Kedatangan Pasien per Jam (Peak Hours)")
        fig1 = px.bar(
            df_analytics, 
            x="Jam Operational", 
            y="Jumlah Pasien", 
            color="Jumlah Pasien",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.subheader("Tren Waktu Tunggu Antrean Pasien")
        fig2 = px.line(
            df_analytics, 
            x="Jam Operational", 
            y="Rata-rata Waktu Tunggu (Menit)",
            markers=True,
            line_shape="spline"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📌 Rekomendasi Solusi Teknik Industri")
    st.success("""
    1. **Bottleneck Mitigation:** Pada pukul 10:00 - 12:00 terjadi *peak hours*, disarankan menambah dokter umum untuk pengalihan kasus ringan.
    2. **Standardization:** Menggunakan data Pre-Triage untuk memotong *setup time* dokter sebesar 30-40%.
    """)