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
    
    # SATÜRN
    st.markdown("---")
    st.write("🪐 **Satürn (Baba/Karma)**")
    saturn_ev = st.number_input("Satürn Kaçıncı Evde?", min_value=1, max_value=12, value=1)
    saturn_burc = st.selectbox("Satürn Burcu", ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"])
    
    # AY (GÜNCELLENDİ: Ev Sorusu Eklendi)
    st.markdown("---")
    st.write("🌙 **Ay (Anne/Duygular)**")
    ay_ev = st.number_input("Ay (Moon) Kaçıncı Evde?", min_value=1, max_value=12, value=1)
    ay_burc = st.selectbox("Ay (Moon) Burcu", ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"])
    
    # Açı Sorusu
    ay_aci = st.checkbox(
        "Ay, Satürn veya Plüton'dan sert açı alıyor mu?",
        help="📌 **İpucu:** Haritanızda Ay ile Satürn/Plüton arasında Kare (90°), Karşıt (180°) veya Kavuşum (0°) varsa işaretleyin."
    )
    
    # 12. EV (GÜNCELLENDİ: Başka Gezegen Sorusu)
    st.markdown("---")
    st.write("👻 **12. Ev (Sırlar ve Dışlanmışlar)**")
    st.info("Haritanızda 12. Evde bulunan gezegenleri seçiniz.")
    gezegenler_12 = st.multiselect(
        "12. Evinizde Hangi Gezegenler Var?",
        ["Yok/Boş", "Güneş", "Ay", "Merkür", "Venüs", "Mars", "Jüpiter", "Satürn", "Plüton", "Uranüs", "Neptün", "Chiron"],
        help="12. Evdeki gezegen, ailede 'kimin' veya 'neyin' saklandığını gösterir."
    )

    st.markdown("---")
    hesapla = st.button("Haritayı ve Reçeteyi Oluştur")

# --- HARİTA VE REÇETE FONKSİYONU ---
def analiz_et():
    # 1. GRAFİK KURULUMU
    G = nx.DiGraph()
    coords = {
        "Karma/Atalar": (0, 4), "BABA": (-1, 2), "ANNE": (1, 2),
        "DANIŞAN": (0, 0), "Dışlanmış Kişi": (2, -1)
    }
    
    # Düğümler
    G.add_node("Karma/Atalar", shape='s', color='#A9A9A9', pos=coords["Karma/Atalar"])
    G.add_node("BABA", shape='s', color='#87CEFA', pos=coords["BABA"])
    G.add_node("ANNE", shape='o', color='#FFB6C1', pos=coords["ANNE"])
    
    danisan_renk = '#87CEFA' if cinsiyet == "Erkek" else '#FFB6C1'
    danisan_sekil = 's' if cinsiyet == "Erkek" else 'o'
    G.add_node("DANIŞAN", shape=danisan_sekil, color=danisan_renk, pos=coords["DANIŞAN"])

    edge_colors = []
    edge_styles = []
    edge_labels = {}
    oneriler = []

    # --- MANTIK MOTORU ---

    # 1. SATÜRN (Baba Karması)
    if saturn_ev in [4, 8, 12] or saturn_burc in ['Oğlak', 'Akrep', 'Koç']:
        G.add_edge("Karma/Atalar", "BABA", color='red')
        edge_colors.append('red'); edge_styles.append('dashed')
        
        sorun = "AĞIR YÜK"
        if saturn_ev == 4: 
            sorun = "KÖK TRAVMASI"
            oneriler.append("🏠 **Satürn 4. Ev:** Baba köklerinde yerleşme sorunu veya göç travması var. Evinizde atalar için bir köşe hazırlayın.")
        if saturn_ev == 8: 
            sorun = "MİRAS/ÖLÜM"
            oneriler.append("💸 **Satürn 8. Ev:** Ailede iflas, miras kavgası veya erken ölüm korkusu var. Bedel ödemek için sadaka verin.")
        if saturn_ev == 12: 
            sorun = "GİZLİ KAYIP"
            oneriler.append("🕯️ **Satürn 12. Ev:** Baba tarafında hapis, hastane veya gizli tutulan bir utanç olabilir. Yargılamadan kabul edin.")
            
        edge_labels[("Karma/Atalar", "BABA")] = sorun
    else:
        G.add_edge("Karma/Atalar", "BABA", color='green')
        edge_colors.append('green'); edge_styles.append('solid')
        oneriler.append("🌳 **Satürn Desteği:** Baba soyundan gelen dayanıklılık mirasına sahipsiniz.")

    # 2. AY (Anne Bağı ve Ev Konumu) - YENİ EKLENDİ
    anne_sorun = False
    
    # Ay Evi Kontrolleri
    if ay_ev == 12:
        anne_sorun = True
        oneriler.append("🌑 **Ay 12. Ev:** Anne sisteme 'uzak' veya 'ulaşılamaz' hissediliyor olabilir. Anne karnındayken yaşanan bir gizli durum (yas, saklanan gebelik) etkin.")
    elif ay_ev == 8:
        anne_sorun = True
        oneriler.append("🦂 **Ay 8. Ev:** Anne ile ilişki 'krizler' üzerinden yürüyor. Kaybetme korkusu veya derin psikolojik bağlar var.")
    elif ay_ev == 4:
        oneriler.append("🏡 **Ay 4. Ev:** Anne evin temel direği. Ancak köklerin yükünü de o taşıyor. Yuvaya aşırı düşkünlük.")

    # Ay Burcu/Açı Kontrolleri
    if ay_burc in ['Oğlak', 'Akrep'] or ay_aci or anne_sorun:
        G.add_edge("ANNE", "DANIŞAN", color='orange')
        edge_colors.append('orange'); edge_styles.append('dotted')
        edge_labels[("ANNE", "DANIŞAN")] = "ANNE YARASI"
        oneriler.append(f"🤱 **Anne Bağı (Ay {ay_burc}):** 'Senin kaderin sana ait anne, ben sadece senin çocuğunum' cümlesini çalışın.")
    else:
        G.add_edge("ANNE", "DANIŞAN", color='green')
        edge_colors.append('green'); edge_styles.append('solid')

    # 3. GÜNEŞ/SATÜRN (Otorite)
    if saturn_ev in [1, 10]:
        G.add_edge("BABA", "DANIŞAN", color='red')
        edge_colors.append('red'); edge_styles.append('solid')
        edge_labels[("BABA", "DANIŞAN")] = "BASKI"
        oneriler.append("👑 **Otorite Sorunu:** Patronlarınızla yaşadığınız sorunlar babanızla ilgilidir.")
    else:
        G.add_edge("BABA", "DANIŞAN", color='green')
        edge_colors.append('green'); edge_styles.append('solid')

    # 4. 12. EV DETAYLI ANALİZİ
    # Eğer Ay Evi 12 girildiyse ama listeden seçilmediyse, otomatik olarak 'Ay' varmış gibi davranalım
    gezegenler_seti = set(gezegenler_12)
    if ay_ev == 12: gezegenler_seti.add("Ay")
    if saturn_ev == 12: gezegenler_seti.add("Satürn")

    if gezegenler_seti and "Yok/Boş" not in gezegenler_seti:
        G.add_node("Dışlanmış Kişi", shape='o', color='#D3D3D3', pos=coords["Dışlanmış Kişi"])
        G.add_edge("Karma/Atalar", "Dışlanmış Kişi", color='gray')
        edge_colors.append('gray'); edge_styles.append('dotted')
        edge_labels[("Karma/Atalar", "Dışlanmış Kişi")] = "GİZLENEN"
        
        G.add_edge("DANIŞAN", "Dışlanmış Kişi", color='gray')
        edge_colors.append('gray'); edge_styles.append('dashed')
        
        st.warning("👻 **12. Ev Analizi (Sırlar):** Bu evdeki gezegenler aile sırlarını gösterir.")
        
        if "Mars" in gezegenler_seti:
            oneriler.append("⚔️ **Mars 12.Ev:** Aile geçmişinde şiddet, savaş travması veya kaza sonucu kayıp saklanıyor.")
        if "Venüs" in gezegenler_seti:
            oneriler.append("💔 **Venüs 12.Ev:** Yasak aşk, kavuşulamayan sevgili veya evlilik dışı çocuk.")
        if "Güneş" in gezegenler_seti:
            oneriler.append("🕵️‍♂️ **Güneş 12.Ev:** Baba veya dede 'kayıp' olabilir. Kimliği (soyadı) değişmiş biri.")
        if "Ay" in gezegenler_seti:
            oneriler.append("🕵️‍♀️ **Ay 12.Ev:** Anne soyundan bir kadın veya yas tutulmamış bir bebek kaybı (kürtaj/düşük) bilinçaltını etkiliyor.")
        if "Satürn" in gezegenler_seti:
            oneriler.append("⚖️ **Satürn 12.Ev:** Otoriteyle ilgili gizli bir utanç (hapis, iflas).")
        if "Plüton" in gezegenler_seti:
            oneriler.append("💀 **Plüton 12.Ev:** Büyük sırlar, taciz veya ağır travmatik sırlar.")
        if "Jüpiter" in gezegenler_seti:
            oneriler.append("⚖️ **Jüpiter 12.Ev:** Göç hikayesi veya dini inançla ilgili saklanan bir durum.")
        if "Uranüs" in gezegenler_seti:
            oneriler.append("⚡ **Uranüs 12.Ev:** Ailede aniden kaybolan veya dışlanan 'delifişek' bir karakter.")

    # --- GÖRSELLEŞTİRME ---
    st.subheader("📊 Sistemik Enerji Haritası")
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.get_node_attributes(G, 'pos')
    colors = nx.get_node_attributes(G, 'color').values()
    
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=colors, edgecolors='black', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, style=edge_styles, width=2, arrowsize=20, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=9, ax=ax)
    ax.axis('off')
    st.pyplot(fig)

    # --- REÇETE BÖLÜMÜ ---
    st.markdown("---")
    st.subheader("💊 Şifa Reçetesi")
    
    for oneri in oneriler:
        if "Uyarı" in oneri or "Dikkate" in oneri or "12. Ev" in oneri: 
             st.warning(oneri)
        elif "Güçlü" in oneri or "Desteği" in oneri:
             st.success(oneri)
        else:
             st.info(oneri)

if hesapla:
    analiz_et()
else:
    st.write("👈 Sol menüden bilgileri girip butona basın.")
