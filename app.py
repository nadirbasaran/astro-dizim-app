import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Sayfa Ayarları
st.set_page_config(page_title="Astro-Sistemik Dizim", page_icon="🔮")

st.title("🔮 Astro-Sistemik Aile Dizimi Haritası")
st.markdown("Astroloji haritanız ve Aile hikayeniz birleşiyor...")

# --- KENAR ÇUBUĞU (VERİ GİRİŞİ) ---
with st.sidebar:
    st.header("1. Kişisel Bilgiler")
    cinsiyet = st.selectbox("Cinsiyetiniz", ["Erkek", "Kadın"])
    
    st.header("2. Astroloji Verileri")
    saturn_ev = st.number_input("Satürn Kaçıncı Evde?", min_value=1, max_value=12, value=1)
    saturn_burc = st.selectbox("Satürn Burcu", ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"])
    
    ay_burc = st.selectbox("Ay (Moon) Burcu", ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"])
    ay_aci = st.checkbox("Ay, Satürn/Plüton'dan sert açı alıyor mu?")
    
    ev_12_gezegen = st.checkbox("12. Evde gezegen var mı?")

    hesapla = st.button("Haritayı Oluştur")

# --- HARİTA ÇİZİM FONKSİYONU ---
def harita_ciz():
    G = nx.DiGraph()
    
    # Koordinatlar
    coords = {
        "Karma/Atalar": (0, 4), 
        "BABA": (-1, 2), 
        "ANNE": (1, 2),
        "DANIŞAN": (0, 0),
        "Dışlanmış Kişi": (2, -1)
    }
    
    # Düğümler
    G.add_node("Karma/Atalar", shape='s', color='#A9A9A9', pos=coords["Karma/Atalar"])
    G.add_node("BABA", shape='s', color='#87CEFA', pos=coords["BABA"])
    G.add_node("ANNE", shape='o', color='#FFB6C1', pos=coords["ANNE"])
    
    # Danışan Rengi
    danisan_renk = '#87CEFA' if cinsiyet == "Erkek" else '#FFB6C1'
    danisan_sekil = 's' if cinsiyet == "Erkek" else 'o'
    G.add_node("DANIŞAN", shape=danisan_sekil, color=danisan_renk, pos=coords["DANIŞAN"])

    edge_colors = []
    edge_styles = []
    edge_labels = {}

    # MANTIK 1: SATÜRN (Baba Karması)
    if saturn_ev in [4, 8, 12] or saturn_burc in ['Oğlak', 'Akrep', 'Koç']:
        G.add_edge("Karma/Atalar", "BABA", color='red')
        edge_colors.append('red')
        edge_styles.append('dashed')
        
        sorun = "AĞIR YÜK"
        if saturn_ev == 4: sorun = "KÖK TRAVMASI (4.EV)"
        if saturn_ev == 8: sorun = "MİRAS/ÖLÜM (8.EV)"
        if saturn_ev == 12: sorun = "GİZLİ KAYIP (12.EV)"
        edge_labels[("Karma/Atalar", "BABA")] = sorun
        st.warning(f"⚠️ **Satürn Uyarısı:** {sorun} tespit edildi. Baba soyunda ağır bir yük olabilir.")
    else:
        G.add_edge("Karma/Atalar", "BABA", color='green')
        edge_colors.append('green')
        edge_styles.append('solid')

    # MANTIK 2: AY (Anne Bağı)
    if ay_burc in ['Oğlak', 'Akrep'] or ay_aci:
        G.add_edge("ANNE", "DANIŞAN", color='orange')
        edge_colors.append('orange')
        edge_styles.append('dotted')
        edge_labels[("ANNE", "DANIŞAN")] = "ANNE YARASI"
        st.warning("⚠️ **Ay Uyarısı:** Anne ile duygusal bağda blokaj veya 'erken büyüme' ihtiyacı.")
    else:
        G.add_edge("ANNE", "DANIŞAN", color='green')
        edge_colors.append('green')
        edge_styles.append('solid')

    # MANTIK 3: GÜNEŞ/SATÜRN (Otorite)
    if saturn_ev in [1, 10]:
        G.add_edge("BABA", "DANIŞAN", color='red')
        edge_colors.append('red')
        edge_styles.append('solid')
        edge_labels[("BABA", "DANIŞAN")] = "BASKI/ÇATIŞMA"
    else:
        G.add_edge("BABA", "DANIŞAN", color='green')
        edge_colors.append('green')
        edge_styles.append('solid')

    # MANTIK 4: 12. EV (Gizli)
    if ev_12_gezegen:
        G.add_node("Dışlanmış Kişi", shape='o', color='#D3D3D3', pos=coords["Dışlanmış Kişi"])
        G.add_edge("Karma/Atalar", "Dışlanmış Kişi", color='gray')
        edge_colors.append('gray')
        edge_styles.append('dotted')
        edge_labels[("Karma/Atalar", "Dışlanmış Kişi")] = "GİZLENEN"
        
        G.add_edge("DANIŞAN", "Dışlanmış Kişi", color='gray')
        edge_colors.append('gray')
        edge_styles.append('dashed')
        st.info("ℹ️ **12. Ev:** Ailede unutulmuş veya dışlanmış biri sisteme etki ediyor olabilir.")

    # ÇİZİM
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.get_node_attributes(G, 'pos')
    colors = nx.get_node_attributes(G, 'color').values()
    
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=colors, edgecolors='black', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, style=edge_styles, width=2, arrowsize=20, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=9, ax=ax)

    ax.axis('off')
    st.pyplot(fig)

if hesapla:
    harita_ciz()
else:
    st.write("👈 Sol taraftaki menüden bilgileri girip 'Haritayı Oluştur' butonuna basın.")
