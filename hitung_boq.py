import streamlit as st
import pandas as pd
from io import BytesIO

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="BoQ Calculator - ECI House",
    page_icon="🏗️",
    layout="wide"
)

# Judul & Sidebar
st.title("🏡 Calculator RAB / BoQ - ECI House")
st.markdown("Aplikasi hitung estimasi biaya konstruksi berdasarkan DED ECI House.")

with st.sidebar:
    st.header("Pengaturan Proyek")
    nama_proyek = st.text_input("Nama Proyek", "Rumah Tinggal ECI House")
    lokasi = st.text_input("Lokasi", "Bandar Lampung")
    kontraktor = st.text_input("Kontraktor/Estimator", "SmartStudio")
    st.divider()
    st.info("💡 **Tips:** Klik dua kali pada sel tabel 'Volume' atau 'Harga Satuan' untuk mengedit nilainya. Total akan update otomatis.")

# ==========================================
# 2. DATA AWAL (DEFAULT)
# ==========================================

# Kita buat fungsi helper untuk bikin dictionary data biar rapi
def create_item(kode, uraian, spek, vol, sat, harga):
    return {
        "Kode": kode,
        "Uraian Pekerjaan": uraian,
        "Spesifikasi": spek,
        "Volume": float(vol),
        "Satuan": sat,
        "Harga Satuan": float(harga),
        "Total Harga": float(vol * harga)
    }

# --- INISIALISASI DATA (SESSION STATE) ---
# Kita simpan data di session_state supaya tidak reset saat user klik sesuatu
if 'data_boq' not in st.session_state:
    st.session_state['data_boq'] = {
        "1. Persiapan & Tanah": [
            create_item("UMUM", "Pembersihan Lahan", "Lokasi Proyek", 200, "m2", 15000),
            create_item("UMUM", "Pematokan & Bowplank", "Kayu Meranti", 80, "m'", 35000),
            create_item("STR-01", "Galian Tanah Pondasi Footplate", "Sesuai gambar", 45, "m3", 95000),
            create_item("STR-02", "Galian Tanah Batu Belah", "Lajur menerus", 30, "m3", 95000),
            create_item("STR-01", "Urugan Pasir Bawah", "t = 5-10 cm", 5, "m3", 250000),
            create_item("UMUM", "Urugan Tanah Kembali", "Dipadatkan", 25, "m3", 35000),
        ],
        "2. Struktur Beton": [
            create_item("STR-01", "Pondasi Footplate F1", "120x120 cm", 19, "Unit", 2500000),
            create_item("STR-01", "Pondasi Footplate F2/F3", "100x100 cm", 10, "Unit", 2000000),
            create_item("STR-02", "Pondasi Batu Belah", "1PC:5PS", 25, "m3", 950000),
            create_item("STR-03", "Sloof S1 (20x40)", "Beton K-250", 6.5, "m3", 3800000),
            create_item("STR-03", "Sloof S2 (15x25)", "Beton K-250", 3.2, "m3", 3800000),
            create_item("STR-08", "Kolom Utama K1 (30x50)", "Isi Volume Manual", 0, "m3", 4200000),
            create_item("STR-08", "Kolom K2 (30x30)", "Isi Volume Manual", 0, "m3", 4200000),
            create_item("STR-04", "Balok B1 (20x40)", "Isi Volume Manual", 0, "m3", 4500000),
            create_item("STR-06", "Plat Dak Atap", "t=15cm + Waterproof", 0, "m3", 4800000),
        ],
        "3. Arsitektur": [
            create_item("ARS-04", "Dinding Bata Merah", "Plester Aci", 450, "m2", 165000),
            create_item("ARS-12", "Lantai Granite Tile", "60x60 Polished", 120, "m2", 350000),
            create_item("ARS-12", "Lantai Keramik Teras", "60x60 Unpolished", 45, "m2", 250000),
            create_item("ARS-15", "Plafond Gypsum", "9mm + Hollow", 140, "m2", 140000),
            create_item("ARS-14", "Batu Alam Fasad", "Andesit/Setara", 25, "m2", 450000),
        ],
        "4. Kusen & Pintu": [
            create_item("KUS-01", "Pintu P1 (Utama)", "Double Swing, Kayu", 2, "Unit", 5500000),
            create_item("KUS-01", "Pintu P2 (Kamar)", "Single Swing", 12, "Unit", 3500000),
            create_item("KUS-02", "Pintu P3 (Lipat)", "Alumunium Kaca", 1, "Unit", 4800000),
            create_item("KUS-06", "Jendela J1", "Swing Double", 4, "Unit", 1800000),
            create_item("KUS-07", "Jendela J3", "Swing Single", 9, "Unit", 1200000),
        ],
        "5. Besi & Kanopi": [
            create_item("ARS-28", "Pagar Gerbang PG1", "Perforated + Hollow", 12, "m2", 1800000),
            create_item("ARS-34", "Kanopi Skylight", "Kaca Tempered 10mm", 8, "m2", 2200000),
            create_item("ARS-30", "Railing Tangga", "Kaca Tempered", 10, "m'", 1500000),
        ],
        "6. MEP (Listrik & Air)": [
            create_item("MEP-01", "Instalasi Air Bersih", "Pipa PVC AW", 1, "Ls", 6500000),
            create_item("MEP-04", "Instalasi Air Kotor", "Pipa PVC D", 1, "Ls", 8500000),
            create_item("MEP-10", "Septictank Biofil", "Kapasitas Besar", 1, "Unit", 5500000),
            create_item("MEP-07", "Titik Lampu", "Downlight + Kabel", 45, "Titik", 275000),
            create_item("MEP-07", "Titik Stop Kontak", "Panasonic + Kabel", 25, "Titik", 285000),
        ]
    }

# ==========================================
# 3. LAYOUT UTAMA (TABS)
# ==========================================

divisi_list = list(st.session_state['data_boq'].keys())
tabs = st.tabs(divisi_list)

grand_total = 0
rekap_per_divisi = {}

for i, tab in enumerate(tabs):
    nama_divisi = divisi_list[i]
    with tab:
        st.subheader(f"📋 {nama_divisi}")
        
        # Konversi list dictionary ke DataFrame
        df = pd.DataFrame(st.session_state['data_boq'][nama_divisi])
        
        # Tampilkan Data Editor (Tabel yang bisa diedit)
        edited_df = st.data_editor(
            df,
            column_config={
                "Harga Satuan": st.column_config.NumberColumn(format="Rp %d"),
                "Total Harga": st.column_config.NumberColumn(format="Rp %d", disabled=True), # Total readonly
            },
            num_rows="dynamic", # User bisa tambah baris
            key=f"editor_{i}",
            use_container_width=True
        )
        
        # Hitung Ulang Total Harga berdasarkan input user
        edited_df["Total Harga"] = edited_df["Volume"] * edited_df["Harga Satuan"]
        
        # Simpan balik ke session state agar perubahan tidak hilang saat pindah tab
        st.session_state['data_boq'][nama_divisi] = edited_df.to_dict('records')
        
        # Tampilkan Subtotal
        subtotal = edited_df["Total Harga"].sum()
        grand_total += subtotal
        rekap_per_divisi[nama_divisi] = subtotal
        
        st.metric(label=f"Subtotal {nama_divisi}", value=f"Rp {subtotal:,.0f}")

# ==========================================
# 4. REKAPITULASI & DOWNLOAD
# ==========================================

st.divider()
st.header("💰 Rekapitulasi Biaya (Grand Total)")

col1, col2 = st.columns([2, 1])

with col1:
    # Bikin DataFrame Rekap
    df_rekap = pd.DataFrame(list(rekap_per_divisi.items()), columns=["Divisi Pekerjaan", "Subtotal"])
    st.dataframe(
        df_rekap, 
        column_config={"Subtotal": st.column_config.NumberColumn(format="Rp %d")},
        use_container_width=True
    )

with col2:
    st.metric(label="TOTAL ESTIMASI BIAYA", value=f"Rp {grand_total:,.0f}")
    
    # --- FITUR DOWNLOAD EXCEL ---
    def to_excel(data_dict, rekap_df, total):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Sheet Rekap
            rekap_df.to_excel(writer, index=False, sheet_name='REKAPITULASI')
            
            # Sheet Detail per Divisi
            for divisi, items in data_dict.items():
                df_div = pd.DataFrame(items)
                sheet_name = divisi.split(".")[1].strip()[:30] # Nama sheet max 31 char
                df_div.to_excel(writer, index=False, sheet_name=sheet_name)
                
        return output.getvalue()

    excel_data = to_excel(st.session_state['data_boq'], df_rekap, grand_total)
    
    st.download_button(
        label="📥 Download Laporan Excel",
        data=excel_data,
        file_name=f"RAB_{nama_proyek.replace(' ', '_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
