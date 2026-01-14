import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Astro-Sistemik Dizim PRO", page_icon="🌌", layout="wide")

st.title("🌌 Astro-Sistemik Aile Dizimi: PRO ANALİZ")
st.markdown("""
Bu modül, doğum haritasındaki **tüm gezegenlerin** hassas konumlarına (Derece/Dakika) göre 
derinlemesine sistemik analiz yapar. Özellikle **29° (Anaretik)** ve **Retro** gezegenler sistemde alarm verir.
""")

# --- YAN MENÜ: DETAYLI VERİ GİRİŞİ ---
with st.sidebar:
    st.header("👤 Danışan Bilgileri")
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
    
    st.markdown("---")
    st.header("🪐 Gezegen Konumları")
    st.info("Lütfen doğum haritasındaki değerleri giriniz.")

    # Gezegen Listesi
    gezegenler_listesi = [
        "Güneş", "Ay", "Merkür", "Venüs", "Mars", 
        "Jüpiter", "Satürn", "Uranüs", "Neptün", "Plüton", 
        "Chiron", "Kuzey Ay Düğümü"
    ]
    
    burclar = ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"]
    
    # Tüm verileri saklayacağımız sözlük
    harita_verileri = {}

    # Otomatik Form Oluşturucu (Her gezegen için)
    for gezegen in gezegenler_listesi:
        with st.expander(f"{gezegen} Bilgileri", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                burc = st.selectbox(f"{gezegen} Burcu", burclar, key=f"{gezegen}_burc")
                ev = st.number_input(f"{gezegen} Evi", 1, 12, 1, key=f"{gezegen}_ev")
            with col2:
                # Düzeltme Burada Yapıldı: format="%02d" eklendi
                derece = st.number_input(f"Derece (°)", 0, 29, 0, key=f"{gezegen}_deg", format="%d")
                dakika = st.number_input(f"Dakika (')", 0, 59, 0, key=f"{gezegen}_min", format="%02d")
            
            is_retro = st.checkbox(f"{gezegen} Retro (R) mu?", key=f"{gezegen}_retro")
            
            # Veriyi kaydet
            harita_verileri[gezegen] = {
                "burc": burc, "ev": ev, 
                "derece": derece, "dakika": dakika, 
                "retro": is_retro
            }

    st.markdown("---")
    hesapla = st.button("🚀 PRO ANALİZİ BAŞLAT", type="primary")

# --- ANALİZ MOTORU ---
def analiz_et():
    # Grafik Hazırlığı
    G = nx.DiGraph()
    coords = {
        "Atalar/Karma": (0, 4), "BABA": (-1.5, 2), "ANNE": (1.5, 2),
        "DANIŞAN": (0, 0), "Dışlanmış": (0, -2)
    }
    
    # Temel Düğümler
    G.add_node("Atalar/Karma", shape='s', color='#808080', pos=coords["Atalar/Karma"])
    G.add_node("BABA", shape='s', color='#87CEFA', pos=coords["BABA"])
    G.add_node("ANNE", shape='o', color='#FFB6C1', pos=coords["ANNE"])
    
    danisan_renk = '#87CEFA' if cinsiyet == "Erkek" else '#FFB6C1'
    G.add_node("DANIŞAN", shape='s' if cinsiyet == "Erkek" else 'o', color=danisan_renk, pos=coords["DANIŞAN"])

    edge_colors = []
    edge_styles = []
    edge_labels = {}
    oneriler = []

    # --- 1. KRİTİK DERECE KONTROLÜ (29° ve 0°) ---
    kritik_gezegenler = []
    for g, veri in harita_verileri.items():
        if veri['derece'] == 29:
            # Çıktı formatı düzeltildi: {veri['dakika']:02d}
            kritik_gezegenler.append(f"{g} (29°{veri['dakika']:02d}')")
            oneriler.append(f"⚠️ **KRİTİK DERECE ({g}):** 29°{veri['dakika']:02d}' derecesi 'Anaretik' derecedir. Aile sisteminde {g} ile temsil edilen konuda 'Tamamlanmamış Bir İş' veya 'Aciliyet' vardır.")
    
    if kritik_gezegenler:
        st.error(f"🚨 **SİSTEM ALARMI:** Şu gezegenler kriz derecesinde: {', '.join(kritik_gezegenler)}")

    # --- 2. SATÜRN ANALİZİ (Baba ve Karma) ---
    saturn = harita_verileri["Satürn"]
    
    if saturn['ev'] in [4, 8, 12] or saturn['burc'] in ['Koç', 'Aslan'] or saturn['retro']:
        G.add_edge("Atalar/Karma", "BABA", color='red')
        edge_colors.append('red')
        edge_styles.append('dashed')
        
        etiket = "AĞIR YÜK"
        if saturn['retro']: etiket += " (RETRO)"
        if saturn['derece'] == 29: etiket += " (KRİZ)"
        
        edge_labels[("Atalar/Karma", "BABA")] = etiket
        
        if saturn['retro']:
            oneriler.append("🪐 **Satürn Retro:** Baba soyundan gelen travma tekrar ediyor. Dedelerde çözülmeyen bir sorun babaya, oradan size geçmiş.")
        
        if saturn['ev'] == 12:
            oneriler.append("👻 **Satürn 12.Ev:** Baba tarafında gizli sırlar, hapishane veya akıl hastanesi geçmişi olabilir.")

    else:
        G.add_edge("Atalar/Karma", "BABA", color='green')
        edge_colors.append('green')
        edge_styles.append('solid')

    # --- 3. AY ANALİZİ (Anne ve Duygular) ---
    ay = harita_verileri["Ay"]
    
    if ay['burc'] in ['Oğlak', 'Akrep'] or ay['ev'] in [8, 12]:
        G.add_edge("ANNE", "DANIŞAN", color='orange')
        edge_colors.append('orange')
        edge_styles.append('dotted')
        
        etiket = "ANNE YARASI"
        if ay['derece'] == 29: etiket = "KOPUK BAĞ"
        edge_labels[("ANNE", "DANIŞAN")] = etiket
        
        # Çıktı formatı düzeltildi
        oneriler.append(f"🌙 **Ay {ay['burc']}:** Anne ile duygusal bağda 'güven' sorunu. (Konum: {ay['derece']}°{ay['dakika']:02d}')")
    else:
        G.add_edge("ANNE", "DANIŞAN", color='green')
        edge_colors.append('green')
        edge_styles.append('solid')

    # --- 4. 12. EV DOLULUĞU (Gizli Şeyler) ---
    ev_12_gezegenler = [g for g, v in harita_verileri.items() if v['ev'] == 12]
    
    if ev_12_gezegenler:
        G.add_node("Dışlanmış", shape='o', color='#D3D3D3', pos=coords["Dışlanmış"])
        G.add_edge("Atalar/Karma", "Dışlanmış", color='gray')
        edge_colors.append('gray')
        edge_styles.append('dotted')
        edge_labels[("Atalar/Karma", "Dışlanmış")] = "GİZLENEN"
        G.add_edge("DANIŞAN", "Dışlanmış", color='gray')
        edge_colors.append('gray')
        edge_styles.append('dashed')
        
        msg = f"👻 **12. Evde Gezegenler Var ({', '.join(ev_12_gezegenler)}):** Sistemde dışlanmış kişiler var."
        st.warning(msg)
        
        if "Mars" in ev_12_gezegenler: oneriler.append("⚔️ **Mars 12.Ev:** Ailede saklanan bir şiddet/askerlik travması.")
        if "Venüs" in ev_12_gezegenler: oneriler.append("💔 **Venüs 12.Ev:** Gizli aşklar veya yasak ilişkiler.")
        if "Plüton" in ev_12_gezegenler: oneriler.append("💀 **Plüton 12.Ev:** Büyük sırlar, iflaslar veya ağır kayıplar.")

    # --- 5. CHIRON (Yaralı Şifacı) ---
    chiron = harita_verileri["Chiron"]
    if chiron['ev'] == 1:
        oneriler.append("🩹 **Chiron 1.Ev:** 'Ben buraya ait miyim?' sorusu. Doğum travması veya istenmeyen çocuk hissi.")
    if chiron['ev'] == 4:
        oneriler.append("🏠 **Chiron 4.Ev:** Aile ocağında derin bir yara. Evin içinde huzur bulamama.")

    # --- 6. GÜNEŞ (Otorite/Baba) ---
    gunes = harita_verileri["Güneş"]
    saturn = harita_verileri["Satürn"] # Yukarıdaki tanımı garantiye alalım
    
    if gunes['ev'] in [8, 12] or (saturn['burc'] == gunes['burc']): 
        G.add_edge("BABA", "DANIŞAN", color='red')
        edge_colors.append('red')
        edge_styles.append('solid')
        edge_labels[("BABA", "DANIŞAN")] = "BASKI"
    else:
        G.add_edge("BABA", "DANIŞAN", color='green')
        edge_colors.append('green')
        edge_styles.append('solid')

    # --- GÖRSELLEŞTİRME ---
    col_graph, col_text = st.columns([2, 1])
    
    with col_graph:
        st.subheader("Sistemik Harita")
        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.get_node_attributes(G, 'pos')
        colors = nx.get_node_attributes(G, 'color').values()
        
        nx.draw_networkx_nodes(G, pos, node_size=2500, node_color=colors, edgecolors='black', ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, style=edge_styles, width=2, arrowsize=20, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8, ax=ax)
        ax.axis('off')
        st.pyplot(fig)

    with col_text:
        st.subheader("📋 Analiz Raporu")
        for i, oneri in enumerate(oneriler, 1):
            if "⚠️" in oneri: st.error(oneri)
            elif "👻" in oneri: st.warning(oneri)
            else: st.info(oneri)

if hesapla:
    analiz_et()
else:
    st.write("👈 Sol menüden tüm gezegenlerin bilgilerini girip 'ANALİZİ BAŞLAT' butonuna basın.")
