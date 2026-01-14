import pandas as pd
from datetime import date

# ==========================================
# 1. KONFIGURASI & KELAS DATA
# ==========================================

class BoQItem:
    def __init__(self, kode, uraian, spesifikasi, satuan, volume_est, harga_satuan=0):
        self.kode = kode            # Referensi Kode Gambar (misal: ARS-01, STR-03)
        self.uraian = uraian        # Nama Pekerjaan
        self.spesifikasi = spesifikasi # Detail spek material/dimensi
        self.satuan = satuan        # Satuan (m2, m3, unit, ls)
        self.volume = volume_est    # Volume estimasi (User harus input real jika 0)
        self.harga_satuan = harga_satuan # Harga satuan (Estimasi)
        self.total_harga = self.volume * self.harga_satuan

def print_header(nama_divisi):
    print("\n" + "="*110)
    print(f"DIVISI PEKERJAAN: {nama_divisi.upper()}")
    print("="*110)

def print_footer(total):
    print("-" * 110)
    print(f"SUBTOTAL: Rp {total:,.2f}")
    print("="*110 + "\n")

# ==========================================
# 2. INPUT DATA BERDASARKAN GAMBAR KERJA (DED ECI.pdf)
# ==========================================

# --- DIVISI 1: PERSIAPAN & TANAH ---
# Referensi: Gambar Situasi & Rencana Pondasi
data_persiapan = [
    BoQItem("UMUM", "Pembersihan Lahan", "Lokasi Proyek", "m2", 200, 15000),
    BoQItem("UMUM", "Pematokan & Bowplank", "Kayu Meranti", "m'", 80, 35000),
    BoQItem("STR-01", "Galian Tanah Pondasi Footplate", "Kedalaman ssuai gambar", "m3", 45, 95000),
    BoQItem("STR-02", "Galian Tanah Pondasi Batu Belah", "Lajur menerus", "m3", 30, 95000),
    BoQItem("STR-01", "Urugan Pasir Bawah Pondasi", "t = 5-10 cm", "m3", 5, 250000),
    BoQItem("STR-01", "Lantai Kerja (Aanstamping)", "Campuran 1:3:5 / Rabat", "m3", 3, 750000),
    BoQItem("UMUM", "Urugan Tanah Kembali", "Dipadatkan", "m3", 25, 35000),
]

# --- DIVISI 2: STRUKTUR BETON (BAWAH & ATAS) ---
# Referensi: STR-01 s/d STR-10 (Denah Pondasi, Sloof, Kolom, Balok)
data_struktur = [
    # Sub-Structure (Pondasi)
    BoQItem("STR-01", "Pondasi Footplate F1", "120x120 cm, Beton Bertulang", "Unit", 19, 2500000), # Jml hitung dari denah
    BoQItem("STR-01", "Pondasi Footplate F2/F3", "100x100 cm, Beton Bertulang", "Unit", 10, 2000000),
    BoQItem("STR-02", "Pondasi Batu Belah", "Camp. 1PC:5PS (Pondasi Menerus)", "m3", 25, 950000),
    
    # Sloof (STR-03)
    BoQItem("STR-03", "Sloof S1", "Beton 20x40 cm, Besi Utama D13", "m3", 6.5, 3800000), # Vol = Pjg x 0.2 x 0.4
    BoQItem("STR-03", "Sloof S2", "Beton 15x25 cm, Besi Utama D13", "m3", 3.2, 3800000),

    # Kolom (STR-08, STR-09)
    BoQItem("STR-08", "Kolom Utama K1", "30x50 cm, Besi 14-D13", "m3", 0, 4200000), # Input Volume
    BoQItem("STR-08", "Kolom K2", "30x30 cm, Besi 8-D13", "m3", 0, 4200000),
    BoQItem("STR-08", "Kolom K3", "15x30 cm, Besi 6-D13", "m3", 0, 4200000),
    BoQItem("STR-08", "Kolom Praktis KP", "15x15 cm, Besi 4-D10", "m'", 0, 150000),

    # Balok (STR-04, STR-05, STR-06)
    BoQItem("STR-04", "Balok B1", "20x40 cm, Besi Utama D13", "m3", 0, 4500000),
    BoQItem("STR-04", "Balok B2", "15x30 cm", "m3", 0, 4500000),
    BoQItem("STR-04", "Balok B3", "15x20 cm", "m3", 0, 4500000),
    
    # Plat & Tangga
    BoQItem("STR-05", "Plat Lantai 2", "Beton Bertulang t=15cm", "m3", 0, 4500000),
    BoQItem("STR-06", "Plat Dak Atap", "Beton Bertulang t=15cm + Waterproofing", "m3", 0, 4800000),
    BoQItem("ARS-30", "Tangga Beton Utama", "Plat & Bordes t=15cm", "m3", 2.5, 4500000),
]

# --- DIVISI 3: ARSITEKTUR (DINDING, LANTAI, PLAFOND) ---
# Referensi: ARS-12 s/d ARS-16 (Denah Pola Lantai & Plafond)
data_arsitektur = [
    # Dinding
    BoQItem("ARS-04", "Pasangan Dinding Bata", "1/2 Bata Merah, Plester, Aci", "m2", 450, 165000),
    BoQItem("ARS-04", "Pasangan Trasram", "Campuran 1:2 (Area Basah)", "m2", 60, 185000),
    BoQItem("ARS-05", "Dinding Roster Beton", "Fasad Depan & Pagar", "m2", 12, 350000),
    BoQItem("ARS-14", "Finishing Batu Alam", "Dinding Fasad Depan (Andesit/Setara)", "m2", 25, 450000),
    
    # Lantai
    BoQItem("ARS-12", "Lantai Granite Tile", "60x60 cm Polished (R.Utama, R.Tamu)", "m2", 120, 350000),
    BoQItem("ARS-12", "Lantai Keramik Teras", "60x60 cm Unpolished/Matt", "m2", 45, 250000),
    BoQItem("ARS-12", "Lantai KM/WC", "40x40 cm Tekstur Kasar", "m2", 35, 220000),
    BoQItem("ARS-12", "Lantai Carport", "Koral Sikat / Batu Ampyang", "m2", 30, 275000),
    
    # Plafond
    BoQItem("ARS-15", "Rangka Plafond Hollow", "Galvanis 40x40 & 20x40", "m2", 180, 140000),
    BoQItem("ARS-15", "Penutup Plafond Gypsum", "9mm (Interior)", "m2", 140, 95000),
    BoQItem("ARS-15", "Penutup Plafond GRC", "6mm (Eksterior/Overstek)", "m2", 40, 95000),
]

# --- DIVISI 4: KUSEN, PINTU, & JENDELA (KOSE & DETAIL) ---
# Referensi: ARS-17 s/d ARS-27 (Detail Kusen Lengkap)
data_kusen = [
    # Pintu (P)
    BoQItem("KUS-01", "Pintu P1 (Utama)", "Swing Double, Alum 4\", Panil Kayu Solid", "Unit", 2, 5500000),
    BoQItem("KUS-01", "Pintu P2 (Kamar)", "Swing Single, Alum 4\", Panil Kayu", "Unit", 12, 3500000),
    BoQItem("KUS-02", "Pintu P3 (Lipat/Folding)", "Alum 4\", Kaca Bening 5mm", "Unit", 1, 4800000),
    BoQItem("KUS-02", "Pintu P4 (KM/WC)", "Swing, Alum 4\", Panil Solid/PVC Premium", "Unit", 5, 2200000),
    BoQItem("KUS-03", "Pintu P5 (Sliding)", "Alum 4\", Kaca Bening 5mm", "Unit", 1, 3800000),
    BoQItem("KUS-03", "Pintu P6 (Lipat/Folding)", "Alum 4\", Kaca Bening 5mm", "Unit", 1, 4800000),
    
    # Pintu Jendela (PJ) & Jendela (J)
    BoQItem("KUS-04", "Pintu Jendela PJ1", "Swing, Kaca 5mm", "Unit", 1, 4200000),
    BoQItem("KUS-04", "Pintu Jendela PJ2", "Swing, Kaca 5mm", "Unit", 2, 4000000),
    BoQItem("KUS-05", "Pintu Jendela PJ3-PJ5", "Swing, Kaca 5mm (R.Kerja/Fitnes)", "Unit", 3, 3800000),
    BoQItem("KUS-06", "Jendela J1", "Swing Double, Kaca 5mm", "Unit", 4, 1800000),
    BoQItem("KUS-06", "Jendela J2", "Swing Triple, Kaca 5mm", "Unit", 3, 2400000),
    BoQItem("KUS-07", "Jendela J3", "Swing Single, Kaca 5mm", "Unit", 9, 1200000),
    BoQItem("KUS-08", "Bouvenlicht BV", "Kaca Mati/Jalusi (Ventilasi)", "Unit", 7, 750000),
]

# --- DIVISI 5: PEKERJAAN BESI & LOGAM (PAGAR & KANOPI) ---
# Referensi: ARS-28, ARS-29, ARS-34, ARS-35
data_besi = [
    BoQItem("ARS-28", "Pagar Gerbang PG1/PG2", "Hollow 50x100 + Plat Perforated 6mm (Folding)", "m2", 12, 1800000), 
    BoQItem("ARS-29", "Pintu Besi PB (Carport)", "Sliding, Hollow + Plat Perforated", "Unit", 1, 6500000),
    BoQItem("ARS-34", "Kanopi Skylight R.Jemur", "Rangka Hollow 50x100 + Kaca Tempered 10mm", "m2", 8, 2200000),
    BoQItem("ARS-35", "Kanopi Taman Belakang", "Rangka Hollow + Kaca Tempered 10mm", "m2", 12, 2200000),
    BoQItem("ARS-30", "Railing Tangga Utama", "Rangka Besi/Stainless + Kaca Tempered", "m'", 10, 1500000),
    BoQItem("ARS-14", "Railing Balkon Depan", "Rangka Besi/Stainless + Kaca Tempered", "m'", 8, 1500000),
]

# --- DIVISI 6: MEKANIKAL, ELEKTRIKAL & PLUMBING (MEP) ---
# Referensi: MEP-01 s/d MEP-13
data_mep = [
    # Sanitasi
    BoQItem("MEP-01", "Instalasi Air Bersih", "Pipa PVC AW 1/2\" & 3/4\"", "Ls", 1, 6500000),
    BoQItem("MEP-04", "Instalasi Air Kotor", "Pipa PVC D 3\" & 4\"", "Ls", 1, 8500000),
    BoQItem("MEP-10", "Septictank Biofil/Beton", "Detail Hal. 66 (Lengkap)", "Unit", 1, 5500000),
    BoQItem("MEP-11", "Sumur Resapan", "Detail Hal. 67 (Ijuk, Kerikil, Bata)", "Unit", 1, 3000000),
    BoQItem("MEP-12", "Bak Kontrol", "Pas. Bata + Tutup Beton (Hal. 69)", "Unit", 4, 650000),
    BoQItem("MEP-13", "Rumah Pompa", "Detail Hal. 68", "Unit", 1, 2000000),
    BoQItem("MEP-01", "Torent Air", "Kapasitas 1000L + Radar", "Unit", 1, 2500000),

    # Elektrikal (Hitung jumlah titik dari denah MEP-07 & MEP-08)
    BoQItem("MEP-07", "Titik Lampu Downlight", "Termasuk Kabel NYM 2x1.5", "Titik", 45, 275000),
    BoQItem("MEP-07", "Titik Stop Kontak", "Termasuk Kabel NYM 3x2.5", "Titik", 25, 285000),
    BoQItem("MEP-07", "Titik Saklar", "Tunggal & Ganda", "Titik", 20, 265000),
    BoQItem("MEP-07", "Box MCB & Sekring", "Presto/Setara", "Unit", 1, 1200000),
]

# ==========================================
# 3. FUNGSI UTAMA (GENERATE REPORT)
# ==========================================

def generate_boq_report():
    print("="*110)
    print(" " * 40 + "BILL OF QUANTITIES (BoQ)")
    print(" " * 35 + "PROYEK: RUMAH TINGGAL ECI HOUSE")
    print(" " * 40 + f"Tanggal: {date.today()}")
    print("="*110)
    
    grand_total = 0
    
    # List of all divisions
    all_divisions = [
        ("I. PEKERJAAN PERSIAPAN & TANAH", data_persiapan),
        ("II. PEKERJAAN STRUKTUR BETON", data_struktur),
        ("III. PEKERJAAN ARSITEKTUR (DINDING/LANTAI)", data_arsitektur),
        ("IV. PEKERJAAN KUSEN PINTU & JENDELA", data_kusen),
        ("V. PEKERJAAN BESI, PAGAR & KANOPI", data_besi),
        ("VI. PEKERJAAN MEP (LISTRIK & SANITASI)", data_mep),
    ]

    # Process each division
    for nama_divisi, daftar_item in all_divisions:
        print_header(nama_divisi)
        
        # Prepare data for DataFrame
        table_data = []
        divisi_total = 0
        
        for item in daftar_item:
            # Recalculate total in case volume changed
            item.total_harga = item.volume * item.harga_satuan
            divisi_total += item.total_harga
            
            table_data.append([
                item.kode,
                item.uraian,
                item.spesifikasi,
                f"{item.volume}",
                item.satuan,
                f"Rp {item.harga_satuan:,.0f}",
                f"Rp {item.total_harga:,.0f}"
            ])
            
        # Create DataFrame
        df = pd.DataFrame(table_data, columns=["REF", "URAIAN PEKERJAAN", "SPESIFIKASI", "VOL", "SAT", "HARGA SAT", "TOTAL HARGA"])
        
        # Print DataFrame nicely
        print(df.to_string(index=False, col_space=12, justify='left'))
        print_footer(divisi_total)
        grand_total += divisi_total

    print("\n" + "#"*110)
    print(f"ESTIMASI TOTAL BIAYA KONSTRUKSI (Grand Total): Rp {grand_total:,.2f}")
    print("#"*110)
    print("\nCatatan:")
    print("1. Volume bernilai '0' harus dihitung manual dari gambar CAD/PDF karena merupakan panjang lari/luas area spesifik.")
    print("2. Harga Satuan adalah estimasi standar. Sesuaikan dengan AHSP lokasi (Bandar Lampung) dan harga pasar terkini.")
    print("3. Item Pagar (Plat Perforated) dan Kanopi (Kaca Tempered) menggunakan material premium, pastikan cek harga supplier.")

if __name__ == "__main__":
    generate_boq_report()
