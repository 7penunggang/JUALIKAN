import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Fungsi untuk menghitung EOQ
def calculate_eoq(demand, ordering_cost, holding_cost):
    eoq = np.sqrt((2 * demand * ordering_cost) / holding_cost)
    return eoq

# Fungsi untuk menghitung total biaya persediaan
def total_inventory_cost(demand, ordering_cost, holding_cost, eoq):
    num_orders = demand / eoq
    total_cost = (num_orders * ordering_cost) + ((eoq / 2) * holding_cost)
    return total_cost, num_orders

# Fungsi untuk menghitung Reorder Point (ROP)
def calculate_rop(demand_weekly, lead_time_weeks):
    return demand_weekly * lead_time_weeks

# Judul aplikasi
st.title("📊 Aplikasi Perhitungan EOQ, ROP dan Visualisasi")
st.subheader("Studi Kasus: Penjualan Ikan Tuna, Kerapu, dan Hiu")

# Input data untuk ketiga jenis ikan
fish_types = ['Tuna', 'Kerapu', 'Hiu']
fish_data = {}

st.sidebar.header("Parameter Global")
days_per_week = st.sidebar.number_input("Hari Operasional per Minggu", value=7, min_value=1)
weeks_per_year = st.sidebar.number_input("Minggu per Tahun", value=52, min_value=1)

for fish in fish_types:
    st.header(f"Data untuk Ikan {fish}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        demand_weekly = st.number_input(f"Permintaan {fish} per Minggu (kg)", min_value=0, key=f"demand_{fish}")
        demand_yearly = demand_weekly * weeks_per_year
        st.markdown(f"**Permintaan Tahunan:** {demand_yearly:,} kg")
    
    with col2:
        ordering_cost = st.number_input(f"Biaya Pemesanan {fish} (IDR)", min_value=0, key=f"order_{fish}")
        holding_cost = st.number_input(f"Biaya Penyimpanan {fish} per kg/tahun (IDR)", min_value=0, key=f"hold_{fish}")
    
    with col3:
        lead_time_weeks = st.number_input(f"Lead Time {fish} (minggu)", min_value=0.0, step=0.1, key=f"lead_{fish}")
        unit_cost = st.number_input(f"Harga Beli {fish} per kg (IDR)", min_value=0, key=f"cost_{fish}")
    
    fish_data[fish] = {
        'demand_weekly': demand_weekly,
        'demand_yearly': demand_yearly,
        'ordering_cost': ordering_cost,
        'holding_cost': holding_cost,
        'lead_time': lead_time_weeks,
        'unit_cost': unit_cost
    }

# Tombol untuk menghitung
if st.button("📈 Hitung EOQ & ROP"):
    results = []
    
    # Membuat figure untuk grafik
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Data untuk tabel perbandingan
    comparison_data = []
    
    for fish in fish_types:
        data = fish_data[fish]
        
        # Hitung EOQ dan ROP
        eoq = calculate_eoq(data['demand_yearly'], data['ordering_cost'], data['holding_cost'])
        total_cost, num_orders = total_inventory_cost(data['demand_yearly'], data['ordering_cost'], 
                                                     data['holding_cost'], eoq)
        rop = calculate_rop(data['demand_weekly'], data['lead_time'])
        
        # Simpan hasil
        results.append({
            'Jenis Ikan': fish,
            'EOQ (kg)': round(eoq, 2),
            'ROP (kg)': round(rop, 2),
            'Frekuensi Pesan/tahun': round(num_orders, 2),
            'Total Biaya Persediaan (IDR)': f"{total_cost:,.2f}",
            'Biaya Pemesanan (IDR)': f"{data['ordering_cost']:,}",
            'Biaya Penyimpanan (IDR/kg/tahun)': f"{data['holding_cost']:,}"
        })
        
        # Persiapkan data untuk grafik
        weeks = np.arange(1, 53)
        inventory = []
        current_stock = eoq
        
        for week in weeks:
            # Pemakaian mingguan
            current_stock -= data['demand_weekly']
            
            # Jika mencapai ROP, lakukan pemesanan
            if current_stock <= rop:
                current_stock += eoq
            
            inventory.append(current_stock)
        
        # Plot grafik level persediaan
        ax1.plot(weeks, inventory, label=fish, marker='o', markersize=4)
        ax1.axhline(y=rop, color='r', linestyle='--', label=f'ROP {fish}')
        
        # Data untuk grafik pie
        eoq_percentage = eoq / sum(calculate_eoq(fish_data[f]['demand_yearly'], 
                                               fish_data[f]['ordering_cost'], 
                                               fish_data[f]['holding_cost']) 
                                for f in fish_types)
        comparison_data.append((fish, eoq_percentage))
    
    # Konfigurasi grafik level persediaan
    ax1.set_title('Level Persediaan per Minggu')
    ax1.set_xlabel('Minggu ke-')
    ax1.set_ylabel('Jumlah Persediaan (kg)')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()
    
    # Konfigurasi grafik perbandingan EOQ
    labels, sizes = zip(*comparison_data)
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    ax2.set_title('Persentase EOQ per Jenis Ikan')
    
    # Tampilkan grafik
    st.header("📊 Visualisasi Inventory Model")
    st.pyplot(fig)
    
    # Tampilkan hasil dalam tabel
    st.header("📋 Hasil Perhitungan")
    df_results = pd.DataFrame(results)
    st.dataframe(df_results.style.format({
        'Biaya Persediaan': "{:,.2f}",
        'Biaya Pemesanan': '{:,.2f}',
        'Biaya Penyimpanan': '{:,.2f}'
    }))
    
    # Penjelasan tentang ROP
    st.subheader("📌 Konsep Reorder Point (ROP)")
    st.write("Reorder Point adalah tingkat persediaan dimana pemesanan baru harus dilakukan. "
             "Perhitungan ROP didasarkan pada:")
    st.latex(r'''ROP = \text{Demand per Minggu} \times \text{Lead Time (minggu)}''')
    st.write("Pada grafik, ROP ditunjukkan dengan garis putus-putus merah. Ketika level persediaan "
             "menyentuh atau melewati garis ini, sistem akan memicu pemesanan baru.")
    
    # Interpretasi hasil
    st.subheader("💡 Interpretasi")
    st.write("1. **EOQ**: Jumlah optimal yang harus dipesan untuk meminimalkan total biaya persediaan")
    st.write("2. **ROP**: Kapan harus melakukan pemesanan ulang")
    st.write("3. **Frekuensi Pesan**: Berapa kali pesanan harus dilakukan dalam setahun")
    st.write("4. **Total Biaya**: Total biaya persediaan (pemesanan + penyimpanan)")
    
    # Rekomendasi strategi inventory
    st.subheader("🚀 Rekomendasi Strategi Persediaan")
    st.write("Berdasarkan hasil perhitungan EOQ dan ROP, berikut rekomendasi strategi pengelolaan persediaan:")
    st.write("- Sesuaikan jumlah pesanan dengan nilai EOQ masing-masing jenis ikan")
    st.write("- Monitor level persediaan secara mingguan untuk menentukan saat tepat melakukan pemesanan ulang")
    st.write("- Pertimbangkan lead time dalam perencanaan pengiriman untuk menghindari stockout")
