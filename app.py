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
    
    # ÖNERİ LİSTESİ (Yeni Özellik)
    oneriler = []

    # --- MANTIK MOTORU ---

    # 1. SATÜRN (Baba Karması)
    if saturn_ev in [4, 8, 12] or saturn_burc in ['Oğlak', 'Akrep', 'Koç']:
        G.add_edge("Karma/Atalar", "BABA", color='red')
        edge_colors.append('red')
        edge_styles.append('dashed')
        
        sorun = "AĞIR YÜK"
        if saturn_ev == 4: 
            sorun = "KÖK TRAVMASI (4.EV)"
            oneriler.append("🏠 **Kökleri Şifalandırma:** Evinizde atalarınız için bir köşe hazırlayın veya onlar adına bir ağaç dikin. 'Sizi görüyorum ve onurlandırıyorum' cümlesini tekrarlayın.")
        if saturn_ev == 8: 
            sorun = "MİRAS/ÖLÜM (8.EV)"
            oneriler.append("💸 **Bedel Ödeme:** Ailede haksız kazanç veya miras sorunu varsa, bir miktar parayı ihtiyaç sahiplerine 'dengelemek adına' dağıtın.")
        if saturn_ev == 12: 
            sorun = "GİZLİ KAYIP (12.EV)"
            oneriler.append("🕯️ **Gizli Olanı Görme:** Ailede unutulmuş, hastaneye yatırılmış veya dışlanmış biri olabilir. Onun için bir mum yakın.")
            
        edge_labels[("Karma/Atalar", "BABA")] = sorun
    else:
        G.add_edge("Karma/Atalar", "BABA", color='green')
        edge_colors.append('green')
        edge_styles.append('solid')
        oneriler.append("🌳 **Baba Desteği:** Satürn konumunuz güçlü. Babanızın veya dedenizin mesleğini veya yeteneğini devam ettirmek size güç katar.")

    # 2. AY (Anne Bağı)
    if ay_burc in ['Oğlak', 'Akrep'] or ay_aci:
        G.add_edge("ANNE", "DANIŞAN", color='orange')
        edge_colors.append('orange')
        edge_styles.append('dotted')
        edge_labels[("ANNE", "DANIŞAN")] = "ANNE YARASI"
        oneriler.append("🤱 **Anne ile Bağ:** Annenizle (hayatta olsun olmasın) içsel bir konuşma yapın. 'Senin kaderin sana ait anne, ben sadece senin çocuğunum' diyerek yükü iade edin.")
    else:
        G.add_edge("ANNE", "DANIŞAN", color='green')
        edge_colors.append('green')
        edge_styles.append('solid')
        oneriler.append("💧 **Duygusal Akış:** Annenizle bağınız sağlıklı görünüyor. Bu akışı korumak için su kenarlarında vakit geçirin.")

    # 3. GÜNEŞ/SATÜRN (Otorite)
    if saturn_ev in [1, 10]:
        G.add_edge("BABA", "DANIŞAN", color='red')
        edge_colors.append('red')
        edge_styles.append('solid')
        edge_labels[("BABA", "DANIŞAN")] = "BASKI/ÇATIŞMA"
        oneriler.append("👑 **Otoriteyle Barış:** İş hayatında patronlarınızla yaşadığınız sorunlar babanızla ilgilidir. Babana içinden 'Sen büyüksün, ben küçüğüm' diyerek hiyerarşiyi kabul et.")
    else:
        G.add_edge("BABA", "DANIŞAN", color='green')
        edge_colors.append('green')
        edge_styles.append('solid')

    # 4. 12. EV (Gizli)
    if ev_12_gezegen:
        G.add_node("Dışlanmış Kişi", shape='o', color='#D3D3D3', pos=coords["Dışlanmış Kişi"])
        G.add_edge("Karma/Atalar", "Dışlanmış Kişi", color='gray')
        edge_colors.append('gray')
        edge_styles.append('dotted')
        edge_labels[("Karma/Atalar", "Dışlanmış Kişi")] = "GİZLENEN"
        
        G.add_edge("DANIŞAN", "Dışlanmış Kişi", color='gray')
        edge_colors.append('gray')
        edge_styles.append('dashed')
        oneriler.append("👻 **Kayıp Parça:** Rüyalarınıza dikkat edin. Ailede yok sayılan birinin enerjisini taşıyor olabilirsiniz. 'Seni görüyorum, sen de bu ailedensin' diyerek onu dahil edin.")

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

    # --- REÇETE BÖLÜMÜ (YENİ) ---
    st.markdown("---")
    st.subheader("💊 Şifa Reçetesi ve Çözüm Önerileri")
    
    for oneri in oneriler:
        if "Uyarı" in oneri or "Dikkate" in oneri: 
             st.warning(oneri)
        elif "Güçlü" in oneri or "Desteği" in oneri:
             st.success(oneri)
        else:
             st.info(oneri)

if hesapla:
    analiz_et()
else:
    st.write("👈 Sol menüden bilgileri girip butona basın.")
