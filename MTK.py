import streamlit as st
import numpy as np

# Fungsi untuk menghitung EOQ
def calculate_eoq(demand, ordering_cost, holding_cost):
    eoq = np.sqrt((2 * demand * ordering_cost) / holding_cost)
    return eoq

# Fungsi untuk menghitung total biaya persediaan
def total_inventory_cost(demand, ordering_cost, holding_cost, eoq):
    num_orders = demand / eoq
    total_cost = (num_orders * ordering_cost) + ((eoq / 2) * holding_cost)
    return total_cost, num_orders

# Judul aplikasi
st.title("Aplikasi Perhitungan EOQ (Economic Order Quantity)")

# Input untuk permintaan tahunan, biaya pemesanan, dan biaya penyimpanan
st.header("Input Data")
demand_tuna = st.number_input("Permintaan Tahunan Tuna (unit)", min_value=0)
ordering_cost_tuna = st.number_input("Biaya Pemesanan Tuna (IDR)", min_value=0)
holding_cost_tuna = st.number_input("Biaya Penyimpanan Tuna (IDR)", min_value=0)

demand_kerapu = st.number_input("Permintaan Tahunan Kerapu (unit)", min_value=0)
ordering_cost_kerapu = st.number_input("Biaya Pemesanan Kerapu (IDR)", min_value=0)
holding_cost_kerapu = st.number_input("Biaya Penyimpanan Kerapu (IDR)", min_value=0)

demand_hiu = st.number_input("Permintaan Tahunan Hiu (unit)", min_value=0)
ordering_cost_hiu = st.number_input("Biaya Pemesanan Hiu (IDR)", min_value=0)
holding_cost_hiu = st.number_input("Biaya Penyimpanan Hiu (IDR)", min_value=0)

# Tombol untuk menghitung EOQ
if st.button("Hitung EOQ"):
    # Hitung EOQ dan total biaya untuk setiap jenis ikan
    eoq_tuna = calculate_eoq(demand_tuna, ordering_cost_tuna, holding_cost_tuna)
    total_cost_tuna, num_orders_tuna = total_inventory_cost(demand_tuna, ordering_cost_tuna, holding_cost_tuna, eoq_tuna)

    eoq_kerapu = calculate_eoq(demand_kerapu, ordering_cost_kerapu, holding_cost_kerapu)
    total_cost_kerapu, num_orders_kerapu = total_inventory_cost(demand_kerapu, ordering_cost_kerapu, holding_cost_kerapu, eoq_kerapu)

    eoq_hiu = calculate_eoq(demand_hiu, ordering_cost_hiu, holding_cost_hiu)
    total_cost_hiu, num_orders_hiu = total_inventory_cost(demand_hiu, ordering_cost_hiu, holding_cost_hiu, eoq_hiu)

    # Tampilkan hasil
    st.header("Hasil Perhitungan")
    st.write(f"**EOQ Tuna:** {eoq_tuna:.2f} unit")
    st.write(f"**Total Biaya Persediaan Tuna:** IDR {total_cost_tuna:.2f}")
    st.write(f"**Jumlah Pemesanan per Tahun Tuna:** {num_orders_tuna:.2f} order")

    st.write(f"**EOQ Kerapu:** {eoq_kerapu:.2f} unit")
    st.write(f"**Total Biaya Persediaan Kerapu:** IDR {total_cost_kerapu:.2f}")
    st.write(f"**Jumlah Pemesanan per Tahun Kerapu:** {num_orders_kerapu:.2f} order")

    st.write(f"**EOQ Hiu:** {eoq_hiu:.2f} unit")
    st.write(f"**Total Biaya Persediaan Hiu:** IDR {total_cost_hiu:.2f}")
    st.write(f"**Jumlah Pemesanan per Tahun Hiu:** {num_orders_hiu:.2f} order")
